from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QSize

import numpy as np
import cv2 as cv

from typing import Optional, List


def fit_to_frame(pixmap: QPixmap, frame: QSize) -> QPixmap:
    """
    :param pixmap: The QPixmap to resize.
    :param frame: The frame within which the image should fit.
    :return: A pixmap fitting inside the given frame.
    """
    frame_width, frame_height = frame.toTuple()
    dw = abs(pixmap.width() - frame_width)
    dh = abs(pixmap.height() - frame_height)
    return pixmap.scaledToWidth(frame_width) if dw > dh else pixmap.scaledToHeight(frame_height)


def load_image(path: str) -> QImage:
    return QImage(path)


def apply_colormap(image: np.ndarray, colormap=cv.COLORMAP_VIRIDIS) -> np.ndarray:
    """
    Normalize array and apply colormap.

    :param numpy.ndarray image: The array to colorize.
    :param cv2.COLORMAP colormap: The colormap to apply.
    :return: Colored array with the given colormap.
    """
    image = image - np.min(image)
    return cv.applyColorMap(np.uint8(255 * (image / np.max(image))), colormap)


def array2d_to_pixmap(array: np.ndarray, normalize=False, colormap: int = cv.COLORMAP_VIRIDIS) -> QPixmap:
    """
    Convert a 2D array (monochrome image) to a QPixmap

    :param numpy.ndarray array: The array to convert.
    :param bool normalize: If `True` then apply colormap.
    :param colormap: Colomap used if normalize is `True`
    :return: QPixmap containing the array.
    """
    assert array.ndim == 2
    if normalize:
        array = apply_colormap(array, colormap)
        height, width, color_bytes = array.shape
        return QPixmap.fromImage(QImage(array.data, width, height, color_bytes * width, QImage.Format_BGR888))
    height, width = array.shape
    return QPixmap.fromImage(QImage(array.data, width, height, width, QImage.Format_Grayscale8))


def array3d_to_pixmap(array: np.ndarray) -> QPixmap:
    """
    Convert a 3D array (color image) to a QPixmap.

    :param array: The array to convert.
    :return: QPixmap containing the array.
    """
    assert array.ndim == 3
    height, width, color_bytes = array.shape
    return QPixmap.fromImage(QImage(array.data, width, height, color_bytes * width, QImage.Format_BGR888))


def create_cluster(layers: List[np.ndarray], normalized=False) -> Optional[np.ndarray]:
    """
    Create a cluster array from a list of layers.

    :param layers: The layers to cluster.
    :param normalized: If `True`, then normalize the resulting array.
    :return: A cluster with each layer on a centroid.
    """
    cluster: Optional[np.ndarray] = None
    for index, layer in enumerate(layers):
        cluster = layer.copy() if cluster is None else cluster + layer * (index + 1)
    return cluster / np.max(cluster) if normalized else cluster
