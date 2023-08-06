from __future__ import annotations

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QMouseEvent
from PySide6.QtCore import Signal

from tat.image_entry import ImageEntry
from tat.layer_data import LayerData

from typing import Final, List


class ClusterImageEntry(ImageEntry):
    """
    Extends ImageEntry. Add a list of LayerData that contains all the cluster layers LayerData.
    """

    double_clicked = Signal(QWidget)

    def __init__(self, parent: QWidget, image: QImage, name: str, image_path: str, array_path: str,
                 layers_data: List[LayerData]):
        """
        Instantiate a ClusterImageEntry object.

        :param parent: The widget calling the method.
        :param image: The image that will be used to draw the preview thumbnail.
        :param image_path: The path of the cluster image.
        :param name: The name that will be showed below the thumbnail.
        :param layers_data: A list of LayerData containing all the information about a layer.
        """
        super(ClusterImageEntry, self).__init__(parent, image, name, image_path, array_path)
        self.layers_data: Final[List[LayerData]] = layers_data

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.double_clicked.emit(self)

    def layer_count(self) -> int:
        return len(self.layers_data)

    def add_layer_data(self, layer_data: LayerData) -> None:
        self.layers_data.append(layer_data)

    def get_layer_data(self, index: int) -> LayerData:
        return self.layers_data[index]

    def remove_layer_data(self, index: int) -> LayerData:
        return self.layers_data.pop(index)
