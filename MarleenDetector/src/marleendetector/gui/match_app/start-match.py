import sys
import os

from PyQt4 import QtGui, QtCore
from matchapp import *

import marleendetector.gallerymanager
from marleendetector.pyfaces import pyfaceswrapper

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.unkownface_location = None
        self.facedir = None
        # connect signals with slots
        QtCore.QObject.connect(self.ui.loadImageButton, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.selectDirButton, QtCore.SIGNAL("clicked()"), self.select_dir)
        QtCore.QObject.connect(self.ui.matchButton, QtCore.SIGNAL("clicked()"), self.matchFace)
    
    def matchFace(self):
        """
            Click event from matchButton
        """
        print "match image with face in selected dir"
        wrapper = pyfaceswrapper.PyFacesWrapper()
        selectedFileName = self.unkownface_location
        selectedDirectoryName = self.facedir
        print selectedFileName
        print selectedDirectoryName
        #selectedFileName = "C:/Documents and Settings/rlindeman/My Documents/TU/PTG/workspace/MarleenDetector/gallery/norm/BARL/BARL_0009_norm_0000.jpg"
        #selectedFileName = marleendetector.gallerymanager.GALLERY_LOCATION + "/norm/BARL/BARL_0009_norm_0000.jpg"
        #selectedDirectoryName = marleendetector.gallerymanager.GALLERY_LOCATION + "/test/sample_dennis"
        print selectedFileName
        print selectedDirectoryName
        
        matchResult = wrapper.recognize(selectedFileName=selectedFileName,selectedDirectoryName=selectedDirectoryName)
        if (matchResult.error is None):
            print matchResult.matchfile
            self.ui.matchImageLabel.setPixmap(QtGui.QPixmap(matchResult.matchfile))
    
    def select_dir(self):
        """
            Click event from selectDirButton
        """
        caption = "Open person directory"
        dir = marleendetector.gallerymanager.GALLERY_NORM
        filter = ""
        options = QtGui.QFileDialog.DirectoryOnly
        dir = QtGui.QFileDialog.getExistingDirectory (self, caption, dir)
        if len(dir) == 0:
            return
        print dir
        self.facedir = str(dir)

    
    def file_dialog(self):
        """
            Click event from loadImageButton
        """
        caption = "Open face image"
        dir = marleendetector.gallerymanager.GALLERY_NORM
        filter = "Images (*.png *.xpm *.jpg)"
        filename = QtGui.QFileDialog.getOpenFileName(self, caption, dir, filter)
        
        if os.path.isfile(filename):
            # a file was selected
            self.unkownface_location = str(filename)
            self.ui.selectedImageLabel.setPixmap(QtGui.QPixmap(filename))
            pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

