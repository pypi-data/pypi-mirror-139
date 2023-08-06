from PySide6.QtWidgets import QWidget, QCheckBox, QSizePolicy
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt, Signal

from tat.image_entry import ImageEntry
from typing import Optional


class CheckableImageEntry(ImageEntry):
    """
    Extends ImageEntry. An ImageEntry with a checkbox under the thumbnail.
    """

    state_changed = Signal(int)

    def __init__(self, parent: QWidget, image: QImage, name: str, image_path: Optional[str] = None,
                 array_path: Optional[str] = None, default_check: bool = True):
        """
        Initialize a CheckableImageEntry

        :param QWidget parent: The parent containing the ImageEntry.
        :param QImage image: The image that will be draw in the thumbnail.
        :param str name: The name that will be shown below the thumbnail. Also used for image basename.
        :param image_path: Path to the image file.
        :type image_path: str, optional
        :param array_path: Path to the Numpy array file.
        :type array_path: str, optional
        :param bool default_check: If True, the checkbox will be checked.
        """
        super(CheckableImageEntry, self).__init__(parent, image, name, image_path, array_path)

        self.__check_box = QCheckBox(self)
        self.__check_box.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.__check_box.setChecked(default_check)
        self.__check_box.stateChanged.connect(self.state_changed)

        self.layout().insertWidget(1, self.__check_box, alignment=Qt.AlignHCenter)

    def isChecked(self) -> bool:
        """
        :return: `True` if checkbox is checked, `False` otherwise.
        :rtype: bool
        """
        return self.__check_box.isChecked()

    def setChecked(self, checked) -> None:
        """
        Changes the entry checkbox state
        :param checked: If `True`, set the checkbox to checked, otherwise set to unchecked.
        """
        self.__check_box.setChecked(checked)
