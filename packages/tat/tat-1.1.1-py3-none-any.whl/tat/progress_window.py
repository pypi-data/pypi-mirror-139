from PySide6.QtWidgets import QDialog, QWidget, QProgressBar
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Signal

from typing import Optional

from tat.ui_progress_bar import Ui_ProgressBar


class ProgressWindow(QDialog):
    """
    Extends QDialog. Create a window with a progress bar and a cancel button.
    """

    cancelled = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__ui = Ui_ProgressBar()
        self.__ui.setupUi(self)
        self.__ui.cancelButton.clicked.connect(self.cancelled)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.cancelled.emit()

    def progress_bar(self) -> QProgressBar:
        return self.__ui.progressBar
