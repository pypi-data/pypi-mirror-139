# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor_window.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_EditorWindow(object):
    def setupUi(self, EditorWindow):
        if not EditorWindow.objectName():
            EditorWindow.setObjectName(u"EditorWindow")
        EditorWindow.resize(800, 600)
        self.centralwidget = QWidget(EditorWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.undoButton = QPushButton(self.centralwidget)
        self.undoButton.setObjectName(u"undoButton")
        self.undoButton.setEnabled(False)

        self.gridLayout_2.addWidget(self.undoButton, 2, 1, 1, 1)

        self.mergeButton = QPushButton(self.centralwidget)
        self.mergeButton.setObjectName(u"mergeButton")

        self.gridLayout_2.addWidget(self.mergeButton, 1, 1, 1, 1)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")

        self.gridLayout_2.addWidget(self.applyButton, 8, 1, 1, 1)

        self.imageFrame = QFrame(self.centralwidget)
        self.imageFrame.setObjectName(u"imageFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageFrame.sizePolicy().hasHeightForWidth())
        self.imageFrame.setSizePolicy(sizePolicy)
        self.imageFrame.setFrameShape(QFrame.StyledPanel)
        self.imageFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.imageFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.imageLabel = QLabel(self.imageFrame)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setMinimumSize(QSize(300, 300))
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.imageLabel, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.imageFrame, 0, 0, 9, 1)

        self.resetButton = QPushButton(self.centralwidget)
        self.resetButton.setObjectName(u"resetButton")

        self.gridLayout_2.addWidget(self.resetButton, 0, 1, 1, 1)

        self.scrollAreaLayers = QScrollArea(self.centralwidget)
        self.scrollAreaLayers.setObjectName(u"scrollAreaLayers")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaLayers.sizePolicy().hasHeightForWidth())
        self.scrollAreaLayers.setSizePolicy(sizePolicy1)
        self.scrollAreaLayers.setMinimumSize(QSize(150, 0))
        self.scrollAreaLayers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaLayers.setWidgetResizable(True)
        self.scrollAreaLayersContents = QWidget()
        self.scrollAreaLayersContents.setObjectName(u"scrollAreaLayersContents")
        self.scrollAreaLayersContents.setGeometry(QRect(0, 0, 148, 452))
        self.verticalLayout = QVBoxLayout(self.scrollAreaLayersContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollAreaLayers.setWidget(self.scrollAreaLayersContents)

        self.gridLayout_2.addWidget(self.scrollAreaLayers, 3, 1, 5, 1)

        EditorWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EditorWindow)

        QMetaObject.connectSlotsByName(EditorWindow)
    # setupUi

    def retranslateUi(self, EditorWindow):
        EditorWindow.setWindowTitle(QCoreApplication.translate("EditorWindow", u"Cluster Editor", None))
        self.undoButton.setText(QCoreApplication.translate("EditorWindow", u"Undo", None))
        self.mergeButton.setText(QCoreApplication.translate("EditorWindow", u"Merge", None))
        self.applyButton.setText(QCoreApplication.translate("EditorWindow", u"Apply to all (save)", None))
        self.imageLabel.setText(QCoreApplication.translate("EditorWindow", u"Layer", None))
        self.resetButton.setText(QCoreApplication.translate("EditorWindow", u"Reset", None))
    # retranslateUi

