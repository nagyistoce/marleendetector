import sys

from PyQt4 import QtGui, QtCore
from util_app import *

from marleendetector.normalizer import *
import marleendetector.gallerymanager


class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # add worker thread
        self.normThread = None # Thread will normalize images
        self.downloadThead = None # Thread will download images from the web
        self.ui.resize_basedirectory_lineEdit.setText(GALLERY_LOCATION)
        self.fillDirectoryList()
        
        # connect signals with slots
        QtCore.QObject.connect(self.ui.normalizeButton, QtCore.SIGNAL("clicked()"), self.normClick)
        QtCore.QObject.connect(self.ui.resizeButton, QtCore.SIGNAL("clicked()"), self.resizeClick)
        
    def fillDirectoryList(self):
        base, dirs, files = iter(os.walk(marleendetector.gallerymanager.GALLERY_LOCATION)).next()
        for dir in dirs:
            self.ui.listWidget.addItem(dir) 
        pass
    
    def normDone(self):
        """
            function called after FaceNormalizer is finished
        """
        self.ui.normalizeButton.setEnabled(True)
        print "Normalizing Done!"
        
    def resizeClick(self):
        """
            Click action on resize button
        """
        sizeStr = str(self.ui.resize_size_lineEdit.text())
        size = DEFAULT_FACE_SIZE
        if len(sizeStr) > 0:
            size = int(sizeStr)

        resizeDirectories = [str(item.text()) for item in self.ui.listWidget.selectedItems()]
        resizer = ImageResizer()
        for directory in resizeDirectories:
            fulldir = marleendetector.gallerymanager.GALLERY_LOCATION + "\\" + directory
            print fulldir
            dirList=filter(lambda fname: fname.endswith(".jpg"), os.listdir(fulldir))
            for fname in dirList:
                fullfilename = fulldir + "\\" + fname
                resizer.resizeImage(fullfilename, fullfilename, size)
        print "done resizing"
    
    def normClick(self):
        """
            Click action on Normalize Button
        """
        print "normalize"
        self.ui.normalizeButton.setEnabled(False) # disable button
        self.ui.progressBar.reset() # reset progressbar

        # get the prefix from the GUI
        prefix = str(self.ui.norm_prefix_lineEdit.text())
        # get the size from the GUI
        sizeN = None
        if len(self.ui.norm_size_lineEdit.text()) > 0:
            # no size given
            sizeN = int(self.ui.norm_size_lineEdit.text())

        # init the Face Normalizer Worker Thread
        self.normThread = NormalizeWorker(prefix=prefix, size=sizeN)
        # NormalizeWorker signals and slots
        self.connect(self.normThread, QtCore.SIGNAL("finished()"), self.normDone)
        self.connect(self.normThread, QtCore.SIGNAL("terminated()"), self.normDone)
        self.connect(self.normThread, QtCore.SIGNAL("imageFinished(int)"), self.ui.progressBar, QtCore.SLOT("setValue(int)"))
        self.connect(self.normThread, QtCore.SIGNAL("startNorm(int)"), self.ui.progressBar, QtCore.SLOT("setMaximum(int)"))
        
        # start the Thread
        self.normThread.start()
                
                
class DownloadWorker(QtCore.QThread):
    """
        The DownloadWorker is a QThread which will download a list of images from the web and save them to a specific directory
    """
    
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)


class NormalizeWorker(QtCore.QThread):
    """
        The NormalizeWorker is a QThread which will normalize a list of images.
        This QThread will emit a SIGNAL before starting and after every image, 
        connect these SLOTs to a progressbar to show the normalization progress.
    """

    def __init__(self, parent = None, prefix=None, size=None):
        """
            Initializes the NormalizeWorker
            creates a FaceNormalizer with the prefix and size as the size of the output images
            sets the Callback functions to send SIGNALS to the progressbar
        """
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.faceNormalizer = FaceNormalizer(prefix)
        self.sizeN = size
        # set callback functions
        self.faceNormalizer.startCallback = self.beforeNormImageStart
        self.faceNormalizer.iterCallback = self.afterNormImage
        
    def beforeNormImageStart(self, totalcount):
        """
            Init the progressbar by sending a QtCore.SIGNAL
        """
        self.emit(QtCore.SIGNAL("startNorm(int)"), totalcount-1)
        
    def afterNormImage(self, index):
        """
            Update progressbar by sending a QtCore.SIGNAL
        """
        self.emit(QtCore.SIGNAL("imageFinished(int)"), index)
        
    def run(self):
        self.faceNormalizer.normalizeFaces(useSize=True, size=self.sizeN)
        
    def __del__(self):
        self.exiting = True
        self.wait()        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())