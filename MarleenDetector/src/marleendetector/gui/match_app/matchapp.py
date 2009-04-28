# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'match-app.ui'
#
# Created: Tue Apr 28 16:16:42 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectedImageLabel = QtGui.QLabel(self.centralwidget)
        self.selectedImageLabel.setGeometry(QtCore.QRect(10, 30, 200, 200))
        self.selectedImageLabel.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.selectedImageLabel.setScaledContents(True)
        self.selectedImageLabel.setObjectName("selectedImageLabel")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label.setObjectName("label")
        self.matchImageLabel = QtGui.QLabel(self.centralwidget)
        self.matchImageLabel.setGeometry(QtCore.QRect(250, 30, 200, 200))
        self.matchImageLabel.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.matchImageLabel.setScaledContents(True)
        self.matchImageLabel.setObjectName("matchImageLabel")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 10, 131, 16))
        self.label_2.setObjectName("label_2")
        self.loadImageButton = QtGui.QPushButton(self.centralwidget)
        self.loadImageButton.setGeometry(QtCore.QRect(10, 240, 75, 23))
        self.loadImageButton.setObjectName("loadImageButton")
        self.matchButton = QtGui.QPushButton(self.centralwidget)
        self.matchButton.setGeometry(QtCore.QRect(250, 240, 75, 23))
        self.matchButton.setObjectName("matchButton")
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(460, 30, 256, 201))
        self.textBrowser.setObjectName("textBrowser")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(460, 10, 46, 14))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.selectedImageLabel.setText(QtGui.QApplication.translate("MainWindow", "selected image", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Selected Image", None, QtGui.QApplication.UnicodeUTF8))
        self.matchImageLabel.setText(QtGui.QApplication.translate("MainWindow", "match image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Matched Image", None, QtGui.QApplication.UnicodeUTF8))
        self.loadImageButton.setText(QtGui.QApplication.translate("MainWindow", "Load Image", None, QtGui.QApplication.UnicodeUTF8))
        self.matchButton.setText(QtGui.QApplication.translate("MainWindow", "Match", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))

