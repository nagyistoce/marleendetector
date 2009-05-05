import pyfacescontroller
import pyfacesgui
import pyeigenfaces
from marleendetector.gallerymanager import *

class MatchResult:
    def __init__(self):
        self.unknownFaceFileName = None
        self.knownFacesDirectoryName = None
        self.error = None
        self.numOfEigenfaces = None
        self.matchfile = None
        self.mindist = None
    
    def updateDisplay(self, error,numOfEigenfaces,matchfile,mindist):
        print "== UPDATE DISPLAY =="
        print "error: " + str(error)
        print "numOfEigenfaces: " + str(numOfEigenfaces)
        print "matchfile: " + str(matchfile)
        print "mindist: " + str(mindist)
        self.error = error
        self.numOfEigenfaces = numOfEigenfaces
        self.matchfile = matchfile
        self.mindist = mindist
        

class PyFacesWrapper:
    
    def __init__(self):
        self.controller=pyfacescontroller.PyFaceController()
        #self.controller=PyFaces.PyFaceController()
        self.controller.myapp = MatchResult()  
    
    def recognize(self, selectedFileName=None, selectedDirectoryName=None):
        # unknown face
        #selectedFileName = GALLERY_LOCATION + "/dennis/ZAS1_0039_norm_0006.jpg"
        #selectedFileName = GALLERY_LOCATION + "/norm/BARL/BARL_0009_norm_0000.jpg"
        # directory with faces
        #selectedDirectoryName = GALLERY_LOCATION + "/test/sample_dennis"
        self.controller.myapp.unknownFaceFileName = selectedFileName
        self.controller.myapp.knownFacesDirectoryName = selectedDirectoryName

        # Threshold value
        thresholdvalue = 2.0
        # Eigen faces
        selectedEigenFaces = 6
        
        self.controller.validateSelection(selectedFileName,selectedDirectoryName,selectedEigenFaces,thresholdvalue)
        return self.controller.myapp # return an object with all result data

if __name__ == "__main__":
    pyfaceWrapper = PyFacesWrapper()
    selectedFileName = GALLERY_LOCATION + "/norm/BARL/BARL_0009_norm_0000.jpg"
    selectedDirectoryName = GALLERY_LOCATION + "/test/sample_dennis"
    data = pyfaceWrapper.recognize(selectedFileName=selectedFileName,selectedDirectoryName=selectedDirectoryName)
    print "Image %s matches %s." % (data.unknownFaceFileName, data.matchfile)
 
    
    