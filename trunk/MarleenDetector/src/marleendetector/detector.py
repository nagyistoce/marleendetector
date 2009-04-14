import sys
from opencv.cv import *
from opencv.highgui import *

from marleendetector.exceptions import *

colour = {}
colour["red"] = CV_RGB(255,0,0)
colour["green"] = CV_RGB(0,255,0)
colour["blue"] = CV_RGB(0,0,255)
colour["yellow"] = CV_RGB(0,255,255)
colour["asd"] = CV_RGB(255,0,255)
colour["ert"] = CV_RGB(255,255,0)
colour["yujyuj"] = CV_RGB(50,255,0)
colour["kgsd"] = CV_RGB(100,5,200)
colour["sdcjr"] = CV_RGB(5,100,200)
colour["qqwer"] = CV_RGB(5,5,100)

class Detector:
    def __init__(self):
        self.cascade = None
        self.storage = cvCreateMemStorage(0)
        
        self.basedir = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\nltk\\opencv\\samples\\c"
        self.cb = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\nltk\\opencv\\data\\haarcascades"
        self.cascade_name = self.cb+"/haarcascade_frontalface_alt.xml"
        self.input_name = self.basedir + "/lena.jpg"
        
        # Parameters for haar detection
        # From the API:
        # The default parameters (scale_factor=1.1, min_neighbors=3, flags=0) are tuned 
        # for accurate yet slow object detection. For a faster operation on real video 
        # images the settings are: 
        # scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
        # min_size=<minimum possible face size
        self.min_size = cvSize(20,20)
        self.image_scale = 1.3
        self.haar_scale = 1.2
        self.min_neighbors = 2
        self.haar_flags = 0
        self.org_image = None # The original image
        self.norm_image = None # the 'normalized' small image
        self.output_image = None # an output image with added graphics
        pass
    
    def generateSmallImage(self):
        # allocate temporary images        
        print "Generating norm image..."
        img = self.org_image
        gray = cvCreateImage(cvSize(img.width,img.height), 8, 1);
        small_img = cvCreateImage(cvSize(cvRound(img.width/self.image_scale),
                                           cvRound(img.height/self.image_scale)), 8, 1 );
    
        # convert color input image to grayscale
        cvCvtColor(img, gray, CV_BGR2GRAY);
        # scale input image for faster processing
        cvResize(gray, small_img, CV_INTER_LINEAR);
        cvEqualizeHist(small_img, small_img);
        cvClearMemStorage(self.storage);
        self.norm_image = small_img # save the 'normalized image'
        #cvNamedWindow("norm image", 1); # generate window to show norm-image
        #cvShowImage( "norm image", self.norm_image ); # show norm image in window
    
    def lookupColourname(self, colourname):
        return colour[colourname]

    def lookupColourindex(self, colourindex):
        return colour.values()[colourindex]
    
    def drawRectangle(self, rectangle):
        # rectangle = (cvPoint(196,223), cvPoint(245,273))
        img = self.output_image
        pt1 = rectangle[0]
        pt2 = rectangle[1]
        #cvRectangle( img, pt1, pt2, CV_RGB(255,50,100), CV_FILLED, 8, 0 );    
        cvRectangle( img, pt1, pt2, CV_RGB(255,50,100), 0, 8, 0 );

    def cropRectangle(self, rectangle, location):
        """
            Cuts an image of size rectangle from the original image and saves it
        """
        image = self.org_image
        pt1 = rectangle[0]
        pt2 = rectangle[1]
        new_width = pt2.x - pt1.x
        new_height = pt2.y - pt1.y
        left = pt1.x
        top = pt1.y
        print "new_width %s, new_height %s, left %s, top %s" % (new_width, new_height, left, top)
        #gray = cvCreateImage(cvSize(img.width,img.height), 8, 1);
        #cvNamedWindow("super face", 1); # generate window for the face
        cropped = cvCreateImage( cvSize(new_width, new_height), 8, 3)
        src_region = cvGetSubRect(self.org_image, cvRect(left, top, new_width, new_height) )
        cvCopy(src_region, cropped)
        #cvShowImage( "super face", cropped ); # show face in window
        #int cvSaveImage( const char* filename, const CvArr* image );
        #filename = self.basedir + "\\crop_face.jpg"
        cvSaveImage(location, cropped)
        
    
    def draw(self, faces, colourname="red", colourindex=None):
        """
            draw faces on original image
        """
        img = self.output_image
        colourvalue = CV_RGB(255,0,0)
        if colourindex != None:
            # use index
            colourvalue = self.lookupColourindex(colourindex)
        else:
            colourvalue = self.lookupColourname(colourname)
            
        if faces:
            for face_rect in faces:
                # the input to cvHaarDetectObjects was resized, so scale the 
                # bounding box of each face and convert it to two CvPoints
                pt1 = cvPoint( int(face_rect.x*self.image_scale), int(face_rect.y*self.image_scale))
                pt2 = cvPoint( int((face_rect.x+face_rect.width)*self.image_scale),
                               int((face_rect.y+face_rect.height)*self.image_scale) )
                #cvRectangle( img, pt1, pt2, CV_RGB(255,0,0), 3, 8, 0 );
                cvRectangle( img, pt1, pt2, colourvalue, 0, 8, 0 );
                #cvRectangle( img, pt1, pt2, colourvalue, -1);
                #print "P1:" + str(pt1)
                #print "P2:" + str(pt2)        
        pass
    
    def showImage(self):
        cvNamedWindow("result", 1);
        cvShowImage( "result", self.output_image);
        #cvWaitKey(0);
        
        #cvDestroyWindow("result");         
    
    def closeWindow(self):
        cvWaitKey(0);
        cvDestroyWindow("result");         
        
    def detectFaces(self):
        """
            Returns the detected faces in self.norm_image
        """
    
        if(self.cascade):
            t = cvGetTickCount();
            faces = cvHaarDetectObjects(self.norm_image, self.cascade, self.storage,
                                         self.haar_scale, self.min_neighbors, self.haar_flags, self.min_size );
            #print faces
            t = cvGetTickCount() - t;
            print "detection time: %gms" % (t/(cvGetTickFrequency()*1000.));
            #self.draw(faces)    
        return faces
    
    def detect_and_draw(self, img):
        # allocate temporary images
        print "Allocating temporary images.."
        self.generateSmallImage()
    
        if(self.cascade):
            t = cvGetTickCount();
            faces = cvHaarDetectObjects(self.norm_image, self.cascade, self.storage,
                                         self.haar_scale, self.min_neighbors, self.haar_flags, self.min_size );
            t = cvGetTickCount() - t;
            print "detection time = %gms" % (t/(cvGetTickFrequency()*1000.));
            #self.draw(faces)
        cvShowImage( "result", img );
    

    
    def initClassifier(self):
        # the OpenCV API says this function is obsolete, but we can't
        # cast the output of cvLoad to a HaarClassifierCascade, so use this anyways
        # the size parameter is ignored
        self.cascade = cvLoadHaarClassifierCascade(self.cascade_name, cvSize(1,1));
        
        if not self.cascade:
            print "ERROR: Could not load classifier cascade"
            sys.exit(-1)
    
    def loadImage(self):
        print "Loading image from file..."            
        self.capture = cvCreateFileCapture(self.input_name); 
    
        #cvNamedWindow("result", 1);
        
        #image = cvLoadImage(self.input_name, 1);
        #self.org_image = image
        self.org_image = cvLoadImage(self.input_name, 1)
        if self.org_image is None:
            # file could not be opened
            raise FileNotFoundError(self.input_name)
        #self.output_image = self.org_image
        self.output_image = cvLoadImage(self.input_name, 1)
        print "width: " + str(self.org_image.width)
        print "height: " + str(self.org_image.height)
    
    def mainM(self):
        
        self.loadImage()
        self.initClassifier()
        
        if(self.org_image):
            self.detect_and_draw(self.org_image);
            cvWaitKey(0);
        
        cvDestroyWindow("result");    

