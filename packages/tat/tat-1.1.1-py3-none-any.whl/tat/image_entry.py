from __future__ import annotations
from typing import Callable, Final, Any, Optional, List
from tat.utils import fit_to_frame
from textwrap import wrap

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QImage, QPixmap, QColor, QMouseEvent
from PySide6.QtCore import Qt, QSize, Signal


class ImageEntry(QWidget):
    """
    Extends QWidget. ImageEntry is a widget that contains a thumbnail and store image information.
    """

    mouse_pressed = Signal(QWidget, QMouseEvent)

    def __init__(self, parent: QWidget, image: QImage, name: str, image_path: Optional[str] = None,
                 array_path: Optional[str] = None):
        """
        Create an ImageEntry

        :param QWidget parent: The parent containing the ImageEntry.
        :param QImage image: The image that will be draw in the thumbnail.
        :param str name: The name that will be shown below the thumbnail. Also used for image basename.
        :param image_path: Path to the image file.
        :type image_path: str, optional
        :param array_path: Path to the Numpy array file.
        :type array_path: str, optional
        """
        super(ImageEntry, self).__init__(parent)
        self.__selected = False
        self.__mouse_pressed_handlers: List[Callable[[ImageEntry, QMouseEvent], Any]] = []
        self.setAutoFillBackground(True)
        self.__default_background_color = self.palette().color(self.backgroundRole())
        self.image_path: Final[Optional[str]] = image_path
        self.array_path: Final[Optional[str]] = array_path
        self.basename: Final[str] = name

        thumbnail = QLabel("Thumbnail", self)
        thumbnail.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        thumbnail.setAlignment(Qt.AlignCenter)
        thumbnail.setPixmap(fit_to_frame(QPixmap.fromImage(image), QSize(50, 50)))

        name_label = QLabel('\n'.join(wrap(name, 15)), self)
        name_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        name_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(thumbnail, alignment=Qt.AlignHCenter)
        layout.addWidget(name_label, alignment=Qt.AlignHCenter)
        self.setLayout(layout)

    def setSelected(self, selected: bool) -> None:
        """
        Set the ImageEntry background to gray if selected is True, else set to the original color.

        :param bool selected: Path to the image file.
        """
        if selected:
            self.__setBackgroundColor(Qt.gray)
            self.__selected = True
            return

        self.__setBackgroundColor(self.__default_background_color)
        self.__selected = False

    def isSelected(self) -> bool:
        """
        :return: True if ImageEntry is currently selected.
        :rtype: bool
        """
        return self.__selected

    def __setBackgroundColor(self, color: QColor) -> None:
        """
        Change the background color to the given parameter.

        :param QColor color:
        """
        pal = self.palette()
        pal.setColor(self.backgroundRole(), color)
        self.setPalette(pal)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.mouse_pressed.emit(self, event)
