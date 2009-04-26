from marleendetector.detector import *
from marleendetector.rectangle_util import *
from marleendetector.gallerymanager import *
import numpy

#image_basedir = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\nltk\\opencv\\samples\\c"
#image_basedir = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\nltk\\opencv\\samples\\images"

h_basedir = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\nltk\\opencv\\data\\haarcascades"

haarconfig = {}
#haarconfig["eye"] =         h_basedir+"\\haarcascade_eye.xml"
#haarconfig["eye_tree"] =    h_basedir+"\\haarcascade_eye_tree_eyeglasses.xml"
haarconfig["alt2"] =        h_basedir+"\\haarcascade_frontalface_alt2.xml"
haarconfig["alt"] =         h_basedir+"\\haarcascade_frontalface_alt.xml"
haarconfig["alt_tree"] =    h_basedir+"\\haarcascade_frontalface_alt_tree.xml"
haarconfig["default"] =     h_basedir+"\\haarcascade_frontalface_default.xml"
#haarconfig["fullbody"] =     h_basedir+"\\haarcascade_fullbody.xml"
#haarconfig["lowerbody"] =     h_basedir+"\\haarcascade_lowerbody.xml"
haarconfig["profileface"] =     h_basedir+"\\haarcascade_profileface.xml"
#haarconfig["upperbody"] =     h_basedir+"\\haarcascade_upperbody.xml"


class FaceDetectorManager:
    """
        This classes manages the various face detectors.
        Provide it with an image and it will use all its haarclassifiers to detect faces. 
    """

    def __init__(self, image_location, prefix, name, output_dir=GALLERY_CROPPED):
        """
            Initializes the FaceDetectorManager, loads the Detector, loads (and formats) the image
            @param image_location: the full path to the image file
            @param prefix: the name of the collection this image belongs to
            @param name: a readable unique name for the image
            @param output_dir: path to the dirctory where the extracted faces will be saved  
        """
        self.name = name # a readable name for the current image
        self.prefix = prefix
        self.detect = Detector() # init the face detector
        self.detect.input_name = image_location # the file with faces
        self.detect.loadImage() # load the image in the detector
        # create the normalized image which will be used to detect faces        
        self.detect.generateSmallImage()
        self.rectangle_list = [] # list of tuples e.g. (point_left_up, point_right_down)
        self.super_faces = []
        self.outputdir = output_dir + "\\" + prefix 
    
    def startDetection(self):
        """
            Loop over all haar classifiers specified and use them to detect faces.
            The face rectangles are saved in the list self.rectangle_list
            It is highly probable that the same face will be found multiple times by different classifiers
        """
        # loop over all haar config's
        for index, haar_key in enumerate(haarconfig):
            haar_location = haarconfig[haar_key]
            print "= ROUND %s: %s =" % (index, haar_key)
            self.detect.cascade_name = haar_location
            self.detect.initClassifier() # init the classifier for the current haarconfig
            faces = self.detect.detectFaces() # detect faces
            face_count = 0
            if faces:
                for face_rect in faces: 
                    # the input to cvHaarDetectObjects was resized, so scale the 
                    # bounding box of each face and convert it to two CvPoints
                    scale = self.detect.image_scale
                    pt1 = cvPoint( int(face_rect.x*scale), int(face_rect.y*scale))
                    pt2 = cvPoint( int((face_rect.x+face_rect.width)*scale),
                                   int((face_rect.y+face_rect.height)*scale) )
                    rect = (pt1, pt2)
                    self.rectangle_list.append(rect) # append the face rectangle to the list
                    face_count = face_count + 1
                    
            print "faces found: " + str(face_count)
            self.detect.draw(faces, colourindex=index) # draw rectangles around the faces
            #detect.showImage()
        print "FACE DETECTION DONE"
        
#detect.showImage()
#print rectangle_list
    def getFaces(self, super_faces=True):
        """
        every face has a list of overlapping rectangles, 
        so if we find every disjunct overlap, we will found the faces
        returns a list of rectangles, list<(cvPoint(lu_x,lu_y), cvPoint(rd_x,rd_y))>
        """
        if super_faces:
            print "Counting distinct faces..."
            disjunct = []
            for rec in self.rectangle_list:
                list = get_overlappingrectangles(rec, self.rectangle_list)
                if list not in disjunct:
                    disjunct.append(list)
            print "distinct faces: " + str(len(disjunct))
            for face_list in disjunct:
                #print "face"
                super_rec = generate_super_rectangle(face_list)
                self.super_faces.append(super_rec)
                self.detect.drawRectangle(super_rec) # draw a rectangle around the face
            return self.super_faces
        else:
            # return all detected faces
            return self.rectangle_list
    
    def saveFacesToFile(self, super_faces=True):
        """
            Crop and save each face to a file
        """
        print "Crop and save face images..."
        faces = []
        if super_faces:
            faces = self.super_faces
        else:
            faces = self.rectangle_list
            
        face_list = []
        for index, face in enumerate(faces):
            #filename = image_basedir + "\\crop_face"+ str(index) +".jpg"
            #filename = "faces\\%s_cropface_%04d.jpg" % (self.name, index)
            filename = "%s_cropface_%04d.jpg" % (self.name, index)
            filepath = self.outputdir + "\\" + filename 
            print filepath
            self.detect.cropRectangle(face, filepath)
            org_image_id = self.name # the name of the current picture: {prefix}_{index}
            face_image_id = index # face index id
            face_rectangle = face # the coordinates of the face
            face_data = (org_image_id, face_image_id, face_rectangle)
            face_list.append(face_data)
        return face_list

    def showResult(self):
        self.detect.showImage() 
        self.detect.closeWindow()


