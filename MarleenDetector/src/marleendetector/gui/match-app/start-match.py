import sys
from os.path import isfile

from PyQt4 import QtGui, QtCore
from matchapp import *

import marleendetector.gallerymanager

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # connect signals with slots
        QtCore.QObject.connect(self.ui.loadImageButton, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.matchButton, QtCore.SIGNAL("clicked()"), self.select_dir)
    
    def select_dir(self):
        caption = "Open person directory"
        dir = marleendetector.gallerymanager.GALLERY_NORM
        filter = ""
        options = QtGui.QFileDialog.DirectoryOnly
        dir = QtGui.QFileDialog.getExistingDirectory (self, caption, dir)
        print dir
        dirList=os.listdir(path)
        for fname in dirList:
            print fname

    
    def file_dialog(self):
        caption = "Open face image"
        dir = marleendetector.gallerymanager.GALLERY_NORM
        filter = "Images (*.png *.xpm *.jpg)"
        filename = QtGui.QFileDialog.getOpenFileName(self, caption, dir, filter)
        
        if isfile(filename):
            # a file was selected
            self.ui.selectedImageLabel.setPixmap(QtGui.QPixmap(filename))
            pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

