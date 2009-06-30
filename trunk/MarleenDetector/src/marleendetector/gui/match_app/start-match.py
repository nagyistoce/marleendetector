# MarleenDetector
# Ricky Lindeman 2009
# 1. Select a normalized image of a person
# 2. Select a dir with images of a single person
# 3. Click match; the image with the minimum distance is calculated
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
        self.matchWorkerThread = None # MatchWorker
        # connect signals with slots
        QtCore.QObject.connect(self.ui.loadImageButton, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.selectDirButton, QtCore.SIGNAL("clicked()"), self.select_dir)
        QtCore.QObject.connect(self.ui.matchButton, QtCore.SIGNAL("clicked()"), self.matchFace)
        
   
    def matchDone(self):
        """
            MatchWorker is finished
        """
        self.ui.matchButton.setEnabled(True)
        self.logline("Matcher finished!");
        if (self.matchWorkerThread.matchResult is not None):
            if (self.matchWorkerThread.matchResult.error is None):
                print self.matchWorkerThread.matchResult.matchfile
                self.ui.matchImageLabel.setPixmap(QtGui.QPixmap(self.matchWorkerThread.matchResult.matchfile))
   
    def matchFace(self):
        """
            Click event from matchButton
        """
        self.ui.matchButton.setEnabled(False)
        
        message = str(10*'=') + "MATCH" + str(10*'=')
        self.logline(message)
        message = "match image with face in selected dir"
        self.logline(message)
        selectedFileName = self.unkownface_location
        selectedDirectoryName = self.facedir
        #print selectedFileName
        #print selectedDirectoryName
        #selectedFileName = "C:/Documents and Settings/rlindeman/My Documents/TU/PTG/workspace/MarleenDetector/gallery/norm/BARL/BARL_0009_norm_0000.jpg"
        #selectedFileName = marleendetector.gallerymanager.GALLERY_LOCATION + "/norm/BARL/BARL_0009_norm_0000.jpg"
        #selectedDirectoryName = marleendetector.gallerymanager.GALLERY_LOCATION + "/test/sample_dennis"
        print selectedFileName # the image with an unknown face
        print selectedDirectoryName # directory with images of the same person
        message = "Selected image %s" % (selectedFileName,)
        self.logline(message)
        message = "Selected dir %s" % (selectedDirectoryName,)
        self.logline(message)


        self.matchWorkerThread = MatchWorker(image=selectedFileName, directory=selectedDirectoryName)
        self.ui.statusbar.showMessage(str("Ready"))
        self.matchWorkerThread.start()
        self.connect(self.matchWorkerThread, QtCore.SIGNAL("finished()"), self.matchDone)
        #self.connect(self.normThread, QtCore.SIGNAL("terminated()"), self.matchDone)
        
        #wrapper = pyfaceswrapper.PyFacesWrapper()
        # find the image with the minimum distance
        #matchResult = wrapper.recognize(selectedFileName=selectedFileName,selectedDirectoryName=selectedDirectoryName)
        #if (matchResult.error is None):
        #    print matchResult.matchfile
        #    self.ui.matchImageLabel.setPixmap(QtGui.QPixmap(matchResult.matchfile))
    
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
        #print dir
        self.facedir = str(dir)
        self.ui.directory_lineEdit.setText(str(dir))

    def logline(self, line):
        """
            Adds a line to the QTextBrowser
        """
        self.ui.textBrowser.append(line)
    
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

class MatchWorker(QtCore.QThread):
    """
        Thread class that will start the pyfaces recognizer
    """
    
    def __init__(self, parent = None, image=None, directory=None):
        QtCore.QThread.__init__(self, parent)
        self.image = image
        self.directory = directory
        self.matchResult = None
        self.exiting = False        
        
    def run(self):
        print "start thread"
        wrapper = pyfaceswrapper.PyFacesWrapper()
        # find the image with the minimum distance
        self.matchResult = wrapper.recognize(selectedFileName=self.image, selectedDirectoryName=self.directory)
        # thread finished
        print "thread finished"
        
    def __del__(self):
        self.exiting = True
        self.wait() 
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = StartQT4()
    window.show()
    sys.exit(app.exec_())

