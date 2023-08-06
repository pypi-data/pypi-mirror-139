from typing import Optional, Union, List, Tuple

import os

import cv2 as cv
import numpy as np

from PySide6.QtWidgets import QLayout, QLabel, QWidget, QGridLayout
from PySide6.QtGui import QImage, QMouseEvent, QCloseEvent, QResizeEvent, QMoveEvent, QPixmap
from PySide6.QtCore import Slot, QSize, QPoint, Qt, Signal

from tat.ui_editor_window import Ui_EditorWindow
from tat.preview_window import PreviewWindow
from tat.cluster_image_entry import ClusterImageEntry
from tat.layer_image_entry import LayerImageEntry
from tat.layer_data import LayerData
from tat.utils import load_image, array2d_to_pixmap, fit_to_frame, create_cluster


class CLusterPreviewWindow(QWidget):
    """
    Extends QWidget. Floating window next to ClusterEditor showing the current cluster state.
    """

    def __init__(self, parent: Optional[QWidget] = None, size: QSize = QSize(600, 600), image: Optional[QImage] = None):
        super(CLusterPreviewWindow, self).__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.resize(size)

        self.imageLabel = QLabel("Cluster Preview", self)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        layout = QGridLayout(self)
        layout.addWidget(self.imageLabel)

        if image is not None:
            self.__update_cluster_preview(QPixmap.fromImage(image))

    def __update_cluster_preview(self, image: QPixmap) -> None:
        self.imageLabel.setPixmap(fit_to_frame(image, QSize(self.width(), self.height())))

    def update_cluster_preview(self, image: Union[np.ndarray, str]) -> None:
        """
        Load an image from a string or an array and update the cluster preview.

        :param image: Can be both a numpy array and a string.
        """
        if isinstance(image, np.ndarray):
            self.__update_cluster_preview(array2d_to_pixmap(image, normalize=True, colormap=cv.COLORMAP_JET))
            return

        if isinstance(image, str):
            self.__update_cluster_preview(QPixmap.fromImage(QImage(image)))
            return

        raise ValueError("Invalid image type: {}".format(type(image)))


class ClusterEditor(PreviewWindow):
    """
    Extends PreviewWindow. The window that allows editing of the clusters.
    """

    applied_to_all = Signal(list)

    def __init__(self, parent: Optional[QWidget], calling_image_entry: ClusterImageEntry):
        super(ClusterEditor, self).__init__(parent)
        self.ui = Ui_EditorWindow()
        self.ui.setupUi(self)
        self.ui.mergeButton.clicked.connect(self.merge)
        self.ui.applyButton.clicked.connect(self.apply_to_all)
        self.ui.resetButton.clicked.connect(self.reset)
        # self.ui.unmergeButton.clicked.connect(self.unmerge)
        self.ui.undoButton.clicked.connect(self.undo)

        self._source_image_entries: List[LayerImageEntry] = []
        self._selected_image_entry: Optional[LayerImageEntry] = None
        self.__cluster_image_entry: ClusterImageEntry = calling_image_entry
        self.__pending_mergers: List[List[int]] = []
        self.__pending_ime: List[LayerImageEntry] = []
        self.__old_entries: List[List[LayerImageEntry]] = []
        self.__cluster_array: np.ndarray = np.load(self.__cluster_image_entry.array_path)

        side_length = self.height() - self.menuBar().height()
        self.__cluster_preview_window = CLusterPreviewWindow(self, QSize(side_length, side_length),
                                                             load_image(self.__cluster_image_entry.image_path))
        # self.cluster_preview_window.show()

        # first = True
        for i in range(self.__cluster_image_entry.layer_count()):
            layer_data = self.__cluster_image_entry.get_layer_data(i)
            array = np.load(layer_data.array_path)
            qim: QImage = load_image(layer_data.image_path)
            ime = LayerImageEntry(self, qim, array, layer_data.name(), is_merger=layer_data.is_merger,
                                  layer_index=layer_data.layer_index, parent_layers=layer_data.parent_layers)
            ime.mouse_pressed.connect(self.image_entry_click_handler)
            ime.state_changed.connect(self.change_merge_button_state)
            self.add_source_image_entry(ime)

            # if first:
            # self.set_preview_image(qim, ime)
            # first = False

    def source_layout(self) -> QLayout:
        return self.ui.scrollAreaLayersContents.layout()

    def image_preview(self) -> QLabel:
        return self.ui.imageLabel

    @Slot(LayerImageEntry, QMouseEvent)
    def image_entry_click_handler(self, sender: LayerImageEntry, event: QMouseEvent) -> None:
        assert type(sender) == LayerImageEntry
        self.set_preview_image(array2d_to_pixmap(sender.array, normalize=True).toImage(), sender)

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self._selected_image_entry is None:
            return
        self.draw_preview_image(array2d_to_pixmap(self._selected_image_entry.array, normalize=True).toImage())

    def moveEvent(self, event: QMoveEvent) -> None:
        position = event.pos()
        self.__cluster_preview_window.move(position - QPoint(self.__cluster_preview_window.width(), 0))
        if self.__cluster_preview_window.isHidden():
            self.__cluster_preview_window.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__cluster_preview_window.close()
        self.__cluster_preview_window = None

    def __pending_add(self, mergers_idx: List[int], ime: LayerImageEntry, old_entries: List[LayerImageEntry]) -> None:
        """
        Add the result of a merge to the pending list, and store the merged layers to be able to undo the merge.

        :param mergers_idx: Indices of the layers to merge.
        :type mergers_idx: list of int
        :param LayerImageEntry ime: The newly merged image entry.
        :param old_entries: A list of the layers used to generate the merged layer.
        :type old_entries: list of LayerImageEntry
        """
        if not self.ui.undoButton.isEnabled():
            self.ui.undoButton.setEnabled(True)
        self.__pending_mergers.append(mergers_idx)
        self.__pending_ime.append(ime)
        self.__old_entries.append(old_entries)

    def __pending_clear(self) -> None:
        """
        Deletes the mergers that haven't been applied yet.
        """
        self.ui.undoButton.setEnabled(False)
        self.__pending_mergers.clear()
        self.__pending_ime.clear()
        self.__old_entries.clear()

    def __pending_count(self) -> int:
        n = len(self.__pending_mergers)
        assert n == len(self.__pending_ime) == len(self.__old_entries)
        return n

    def __pending_pop(self) -> Tuple[List[int], LayerImageEntry, List[LayerImageEntry]]:
        """
        Gives a tuple of the last merged indices, image entry of the merged layers and the list of image entries
        used to generate the merger.

        :rtype: (list of int, LayerImageEntry, list of LayerImageEntry)
        """
        if self.__pending_count() == 1:
            self.ui.undoButton.setEnabled(False)
        return self.__pending_mergers.pop(), self.__pending_ime.pop(), self.__old_entries.pop()

    @Slot(int)
    def change_merge_button_state(self, state: int) -> None:
        if not state == Qt.CheckState.Checked:
            self.ui.mergeButton.setEnabled(True)
            return
        if len(self.get_selected_entries()) == len(self._source_image_entries):
            self.ui.mergeButton.setEnabled(False)

    @Slot()
    def merge(self) -> None:
        """
        Merge the selected layers only in the current view. Update the cluster preview with the newly merged cluster.
        """
        if len(self.get_selected_entries()) < 2:
            return
        checked_indices: List[int] = []
        old_ime: List[LayerImageEntry] = []
        merger: Optional[np.ndarray] = None
        parent_layers: List[int] = []
        for index, ime in enumerate(self._source_image_entries):
            if not ime.isChecked():
                continue

            if ime.layer_data.is_merger:
                assert ime.layer_data.parent_layers is not None
                parent_layers.extend(ime.layer_data.parent_layers)
            else:
                assert ime.layer_data.layer_index is not None
                parent_layers.append(ime.layer_data.layer_index)

            checked_indices.append(index)
            old_ime.append(ime)
            merger = self._source_image_entries[index].array if merger is None else merger | self._source_image_entries[
                index].array
            ime.setChecked(False)
            ime.close()

        for i in sorted(checked_indices, reverse=True):
            self._source_image_entries.pop(i)

        self.__cluster_array = create_cluster([ime.array for ime in self._source_image_entries])
        self.__cluster_preview_window.update_cluster_preview(self.__cluster_array)

        qim: QImage = array2d_to_pixmap(merger, normalize=True).toImage()
        merged_ime = LayerImageEntry(self, qim, merger, f"m {LayerData.indices2str(parent_layers)}",
                                     is_merger=True, parent_layers=parent_layers)
        merged_ime.mouse_pressed.connect(self.image_entry_click_handler)
        merged_ime.state_changed.connect(self.change_merge_button_state)
        self.__pending_add(checked_indices, merged_ime, old_ime)
        self.set_preview_image(qim, merged_ime)
        self.add_source_image_entry(merged_ime)
        self.change_all_entries_check_state(False)

    @Slot()
    def apply_to_all(self) -> None:
        """
        Send a merge signal for each pending merge.
        """
        for merger in self.__pending_mergers:
            self.applied_to_all.emit(merger)
        self.__pending_clear()

    @Slot()
    def reset(self) -> None:
        """
        Removes all uncommitted changes done in the editor.
        """
        if len(self.__pending_mergers) == 0:
            return

        self.__pending_clear()

        for ime in self._source_image_entries:
            ime.close()

        self._source_image_entries.clear()

        self.__cluster_array = np.load(self.__cluster_image_entry.array_path)
        self.__cluster_preview_window.update_cluster_preview(self.__cluster_array)

        for i in range(self.__cluster_image_entry.layer_count()):
            layer_data = self.__cluster_image_entry.get_layer_data(i)
            array = np.load(layer_data.array_path)
            qim: QImage = load_image(layer_data.image_path)
            ime = LayerImageEntry(self, qim, array, layer_data.name(), layer_data.is_merger, layer_data.layer_index,
                                  layer_data.parent_layers)
            ime.mouse_pressed.connect(self.image_entry_click_handler)
            ime.state_changed.connect(self.change_merge_button_state)
            self.add_source_image_entry(ime)
            if i == 0:
                self.set_preview_image(load_image(layer_data.image_path), ime)
        self.change_all_entries_check_state(False)

    @Slot()
    def unmerge(self) -> None:
        """
        Unmerge the selected layers in the editor. Global behavior not implemented.
        """
        for index, ime in enumerate(self._source_image_entries):
            if not ime.isChecked() or not ime.layer_data.is_merger:
                continue

            self._source_image_entries.pop(index)
            assert ime.layer_data.parent_layers is not None
            for parent_layer_index in ime.layer_data.parent_layers.copy():
                directory = os.path.dirname(self.__cluster_image_entry.image_path)
                path_no_ext = os.path.join(directory,
                                           f"{self.__cluster_image_entry.basename}_layer_{parent_layer_index}")
                image_path = f"{path_no_ext}.png"
                array_path = f"{path_no_ext}.npy"
                parent_ime = LayerImageEntry(self, load_image(image_path), np.load(array_path), str(parent_layer_index),
                                             layer_index=parent_layer_index)
                parent_ime.mouse_pressed.connect(self.image_entry_click_handler)
                parent_ime.state_changed.connect(self.change_merge_button_state)
                self.add_source_image_entry(parent_ime)
            ime.close()

    @Slot()
    def undo(self) -> None:
        """
        Go one step back.
        """
        if self.__pending_count() == 0:
            return

        indices, pending_ime, old_ime = self.__pending_pop()
        self._source_image_entries.pop()

        pending_ime.close()

        for index, ime in zip(indices, old_ime):
            ime.setVisible(True)
            self.add_source_image_entry(ime, index)
        self.image_preview().setText("Layer")
        self.__cluster_preview_window.update_cluster_preview(self.__cluster_image_entry.image_path)
        self.change_all_entries_check_state(False)
