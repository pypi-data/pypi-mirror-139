from typing import Optional, Final, List

import numpy as np

from tat.checkable_image_entry import CheckableImageEntry
from tat.layer_data import LayerData

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage


class LayerImageEntry(CheckableImageEntry):
    """
    Extends CheckableImageEntry. Add a LayerData and an array-like to a CheckableImageEntry.
    """

    def __init__(self, parent: QWidget, image: QImage, array: np.ndarray, name: str, is_merger: bool = False,
                 layer_index: Optional[int] = None, parent_layers: Optional[List[int]] = None):
        """

        :param QWidget parent: The parent containing the ImageEntry.
        :param QImage image: The image that will be draw in the thumbnail.
        :param numpy.ndarray array: Array of the image.
        :param str name: The name that will be shown below the thumbnail. Also used for image basename.
        :param bool is_merger: Tells if the layer a merger of multiple layers or not.
        :param layer_index: Index of the layer if it is not a merger.
        :type layer_index: int, optional
        :param parent_layers: List of the parent layers if the layer is a merger.
        :type parent_layers: list of int, optional
        """
        super(LayerImageEntry, self).__init__(parent, image, name, default_check=False)

        self.array: Final[np.ndarray] = array
        self.layer_data: Final[LayerData] = LayerData(is_merger=is_merger, layer_index=layer_index,
                                                      parent_layers=parent_layers)
