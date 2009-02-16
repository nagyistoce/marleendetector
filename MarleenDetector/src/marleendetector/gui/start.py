import sys
from PyQt4 import QtCore, QtGui
from facestrainer import *
from marleendetector.faces.facesdb import *

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        self.fdbManager = FacesDBManager() # reads all person names from a file
           
        personListModel = PersonListModel(self.fdbManager.persons, self)
        self.ui.personListView.setModel(personListModel)
        
        # the label will show the normalized face
        #self.ui.faceLabel.setScaledContents(True)
        self.ui.faceLabel.setGeometry(QtCore.QRect(180, 20, 150, 150))
        # get all the norm-face locations
        self.face_locations = getNormFaceImages()
        self.face_iter = self.face_locations.__iter__()

        # load the first face
        self.current_image_id = None
        self.loadNextImage()

        # here we connect signals with our slots
        QtCore.QObject.connect(self.ui.nextButton, QtCore.SIGNAL("clicked()"), self.nextImage)
        QtCore.QObject.connect(self.ui.saveResultButton, QtCore.SIGNAL("clicked()"), self.saveResults)
        QtCore.QObject.connect(self.ui.personListView, QtCore.SIGNAL("pressed(QModelindex)"), self.key_pressed)
        QtCore.QObject.connect(self.ui.personListView, QtCore.SIGNAL("doubleClicked(QModelindex *)"), self.double_clicked)
        QtCore.QObject.connect(self.ui.personListView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.ui.nextButton.click)


    def key_pressed(self):
        print "pressed key"
    
    def double_clicked(self):
        print "double_clicked"
        
    def nextImage(self):
        print "next"
        selection =  self.ui.personListView.selectedIndexes()
        if len(selection) > 0:
            # an item was selected from the list
            for sel in selection:
                #print sel.row()
                print str(self.fdbManager.persons[sel.row()])
                print self.current_image_id
                #print sel.column()
            self.loadNextImage()
        else:
            # no item was selected
            # TODO: use the name specified in the inputbox
            pass
            
    def loadNextImage(self):
        print "Loading next image..."
        try:
            next_image_location = self.face_iter.next() # get the next face from the list
            self.current_image_id = next_image_location
            img = GALLERY_NORM + "\\" + next_image_location
            self.ui.faceLabel.setPixmap(QtGui.QPixmap(img))
        except StopIteration:
            print "No more faces..."

            
    def saveResults(self):
        print "save"

class PersonListModel(QtCore.QAbstractListModel): 
    def __init__(self, datain, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QtCore.QAbstractTableModel.__init__(self, parent, *args) 
        self.listdata = datain
 
    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            value = str(self.listdata[index.row()].name)
            return QtCore.QVariant(value)
        else: 
            return QtCore.QVariant()         

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

