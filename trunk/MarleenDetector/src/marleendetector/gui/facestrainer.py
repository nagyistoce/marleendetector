# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'facetrainer.ui'
#
# Created: Mon Feb 16 23:46:40 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 313)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.personListView = QtGui.QListView(self.centralwidget)
        self.personListView.setGeometry(QtCore.QRect(10, 10, 160, 220))
        self.personListView.setObjectName("personListView")
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(180, 210, 75, 20))
        self.nextButton.setObjectName("nextButton")
        self.saveResultButton = QtGui.QPushButton(self.centralwidget)
        self.saveResultButton.setGeometry(QtCore.QRect(350, 220, 75, 23))
        self.saveResultButton.setObjectName("saveResultButton")
        self.faceLabel = QtGui.QLabel(self.centralwidget)
        self.faceLabel.setGeometry(QtCore.QRect(200, 20, 161, 141))
        self.faceLabel.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.faceLabel.setMidLineWidth(4)
        self.faceLabel.setScaledContents(True)
        self.faceLabel.setObjectName("faceLabel")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 240, 161, 20))
        self.lineEdit.setMaxLength(25)
        self.lineEdit.setObjectName("lineEdit")
        self.newPersonButton = QtGui.QPushButton(self.centralwidget)
        self.newPersonButton.setGeometry(QtCore.QRect(180, 240, 75, 20))
        self.newPersonButton.setObjectName("newPersonButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setBaseSize(QtCore.QSize(0, 0))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.personListView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.nextButton.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Marleen Detector", None, QtGui.QApplication.UnicodeUTF8))
        self.nextButton.setText(QtGui.QApplication.translate("MainWindow", "Next Face", None, QtGui.QApplication.UnicodeUTF8))
        self.saveResultButton.setText(QtGui.QApplication.translate("MainWindow", "Save Result", None, QtGui.QApplication.UnicodeUTF8))
        self.newPersonButton.setText(QtGui.QApplication.translate("MainWindow", "New Person", None, QtGui.QApplication.UnicodeUTF8))
        self.statusbar.setStatusTip(QtGui.QApplication.translate("MainWindow", "Marleen Detector", None, QtGui.QApplication.UnicodeUTF8))

