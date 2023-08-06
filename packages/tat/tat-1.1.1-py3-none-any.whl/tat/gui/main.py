from typing import Optional, List
import sys
from PySide6.QtWidgets import QApplication
from tat.main_window import MainWindow


def main(args: Optional[List[str]] = None) -> int:
    if args is None:
        args = sys.argv[1:]
    # args is currently not used

    app = QApplication()
    app.main_window = MainWindow()
    app.main_window.show()
    return app.exec()
