from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QLayout
from PySide6.QtGui import QImage, QResizeEvent, QPixmap, QMouseEvent
from PySide6.QtCore import QSize, Slot

from abc import abstractmethod
from typing import Optional, List

from tat.image_entry import ImageEntry
from tat.checkable_image_entry import CheckableImageEntry
from tat.utils import load_image, fit_to_frame


class PreviewWindow(QMainWindow):
    """
    Extends QMainWindow. An interface to easily create a window class containing a preview area and a source image
    entries area.
    """

    def __init__(self, parent: Optional[QWidget]):
        super(PreviewWindow, self).__init__(parent)
        self._selected_image_entry: Optional[ImageEntry] = None
        self._source_image_entries: List[CheckableImageEntry] = []

    @abstractmethod
    def image_preview(self) -> QLabel:
        """
        Override this method to return the image preview QLabel.

        :rtype: QLabel
        """
        raise NotImplementedError

    @abstractmethod
    def source_layout(self) -> QLayout:
        """
        Override this method to return the source area container layout.

        :rtype: QLayout
        """
        raise NotImplementedError

    def add_source_image_entry(self, ime: CheckableImageEntry, index: Optional[int] = None) -> None:
        """
        Add an image entry in the source area and `_source_image_entries`.

        :type ime: CheckableImageEntry
        :param index: if set, insert the image entry in `_source_image_entries` at the given index, otherwise \
        append at the end.
        :type index: int, optional
        """
        self._source_image_entries.append(ime) if index is None else self._source_image_entries.insert(index, ime)
        self.source_layout().addWidget(ime)

    def draw_preview_image(self, image: QImage) -> None:
        """
        Draw the given image in the preview area.

        :type image: QImage
        """
        image_preview = self.image_preview()
        image_preview.setPixmap(
            fit_to_frame(QPixmap.fromImage(image), QSize(image_preview.width(), image_preview.height())))

    def set_preview_image(self, image: QImage, image_entry: ImageEntry) -> None:
        """
        Set the given image entry as selected and draw the corresponding image.

        :rtype: object
        """
        if image_entry is self._selected_image_entry:
            return

        self.draw_preview_image(image)
        if self._selected_image_entry is not None:
            self._selected_image_entry.setSelected(False)
        self._selected_image_entry = image_entry
        image_entry.setSelected(True)

    def clear_preview_image(self) -> None:
        """
        Replace the preview image with the text `Preview` and deselect image entry if any.
        """
        self.image_preview().setText("Preview")
        if self._selected_image_entry is not None:
            self._selected_image_entry.setSelected(False)
        self._selected_image_entry = None

    @Slot(ImageEntry, QMouseEvent)
    def image_entry_click_handler(self, sender: ImageEntry, event: QMouseEvent) -> None:
        self.set_preview_image(load_image(sender.image_path), sender)

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self._selected_image_entry is None:
            return
        self.draw_preview_image(load_image(self._selected_image_entry.image_path))

    def clear_image_entries(self) -> None:
        """
        Remove all the image entries in the source area. Clear `_source_image_entries`.
        """
        for ime in self._source_image_entries:
            ime.close()
        self._source_image_entries.clear()

    def select_deselect(self) -> None:
        """
        If all images are not checked, check them all, otherwise uncheck all.
        """
        all_checked = True
        for ime in self._source_image_entries:
            if not ime.isChecked():
                all_checked = False
                break

        for ime in self._source_image_entries:
            ime.setChecked(not all_checked)

    def get_selected_entries(self) -> List[CheckableImageEntry]:
        """
        Return a list of checked image entries.

        :rtype: list of CheckableImageEntry
        """
        selected: List[CheckableImageEntry] = []
        for ime in self._source_image_entries:
            if ime.isChecked():
                selected.append(ime)
        return selected

    def change_all_entries_check_state(self, checked: bool) -> None:
        """
        Set all image entries to the given check state.

        :param bool checked: Change all to this state.
        """
        for ime in self.get_selected_entries():
            ime.setChecked(checked)
