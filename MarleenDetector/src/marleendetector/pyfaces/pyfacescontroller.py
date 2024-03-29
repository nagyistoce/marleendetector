import pyfacesgui
import pyeigenfaces
from Tix import Tk
from os.path import basename
from string import split
import traceback
import sys

class PyFaceController(object):
    def __init__(self):
        print "controller()"
        self.facet = pyeigenfaces.egface()
            
    def getExtension(self, fileName):
        """
            Returns the extension of the filename
        """
        print 'getExtension():'       
        extension = split(basename(fileName), '.')[1]
        return extension
    
    def validateSelection(self, fileName, directoryName, numOfEigenfaces, thresholdVal):
        """
            1. validates the filename and the directory
            2. validate the images in the directory
            3. execute the algorithm
            
            @param numOfEigenfaces: the number of eigen faces that will be used
            @param thresholdVal: the threshild value for the minimum distance
        """
        print 'validateSel()::filename=', fileName, 'dir=:', directoryName, 'thresh=:', thresholdVal, 'numOfEigenfaces=:', numOfEigenfaces        
        
        if fileName is '':
            print 'validateSelection()::no file selected!!'
            error = pyfacesgui.NoFileSelectError('no file selected')
            self.updateResults(error)
        elif directoryName is '':
            print 'validateSelection()::no directory selected!!'
            error = pyfacesgui.NoDirSelectError('no directory selected')
            self.updateResults(error)
        else:
            # filename and directory contents OK
            extension = self.getExtension(fileName) # get the extension of the selected image            
            dirParser = pyeigenfaces.DirectoryParser(directoryName) # create a Directory Parser for the selected directory
            imagefilenames = dirParser.parseDirectory(extension) # fetch image names that have the same extension as the selected image
            if(not self.facet.isValid(numOfEigenfaces, len(imagefilenames))):
                numOfEigenfaces = len(imagefilenames) / 2
            #self.recogniseFace(imagefilenames,fileName,directoryName,numOfEigenfaces,thresholdVal)                                
            try:
                self.recogniseFace(imagefilenames, fileName, directoryName, numOfEigenfaces, thresholdVal)
            except Exception, inst:
                print "Exception: " + str(inst)
                traceback.print_exc(file=sys.stdout)

                self.updateResults(inst, numOfEigenfaces)        
    
    def recogniseFace(self, imagefilenames, selectedFileName, selectedDirectory, numOfEigenfaces, thresholdVal):
        """
            Tries to recognize the image by calculating eigenfaces from the images in the directory
            @param imagefilenames: list of image filenames
            @param selectedFileName: the selected image
            @param selectedDirectory: path of the selected directory
            @param numOfEigenfaces: number of eigen faces
        """
        print 'recogniseFace()::'
        self.facet.checkCache(selectedDirectory, imagefilenames, numOfEigenfaces)
        mindist, matchfile = self.facet.findMatchingImage(selectedFileName, numOfEigenfaces, thresholdVal)
        self.processMatchResult(matchfile, mindist, numOfEigenfaces)        
    
    def processMatchResult(self, matchfile, mindist, numOfEigenfaces):
        if not matchfile:
            error = pyeigenfaces.NoMatchError('No match! try higher threshold')            
            self.updateResults(error, numOfEigenfaces)
        else:
            print "processMatchResult()::matches :" + matchfile + " dist :" + str(mindist)#            
            self.updateResults(None, numOfEigenfaces, matchfile, mindist) 
        
    def updateResults(self, error, numOfEigenfaces=0, matchfile='', mindist=0.0):
        print 'updateResults()::'
        self.myapp.updateDisplay(error, numOfEigenfaces, matchfile, mindist)        
        
if __name__ == "__main__":
    controller = PyFaceController()    
    root = Tk()
    root.wm_title("PyFaces")
    controller.myapp = pyfacesgui.PyFaceUI(root, controller)
    root.mainloop()
    
 
    
    
    
