# normalizes the extracted faces and resizes them
import os
import re

from opencv import cv
from opencv import highgui

from marleendetector.gallerymanager import *



NORM_FILENAME = "norm_%04d.jpg"
DEFAULT_FACE_SIZE = 200


class FaceNormalizer:
    """
        The FaceNormalizer normalizes the cropped_face_images to a standard size and gray-scale
    """
    
    def __init__(self, prefix, cropped_faces_dir=GALLERY_CROPPED, norm_dir=GALLERY_NORM):
        """
        Initializes the FaceNormalizer,
        prefix the name of the image collection
        set cropped_faces_dir to link to the directory containing all the cropped faces
        set norm_dir to the directory where the normalized images should be saved
        """
        self.prefix = prefix
        self.cropped_faces_dir = cropped_faces_dir + "\\" + prefix # non normalized faces location
        self.norm_dir = norm_dir + "\\" + prefix # normalized faces dir
        self.startCallback = None # function to call before normalizing
        self.iterCallback = None # function to call after every image
        self.filecount = 0
        self.index = 0
    
    def getCroppedFaceImages(self):
        """
            Returns a list of all the croppedfaces filename
        """
        dirList = os.listdir(self.cropped_faces_dir) # all files in the dir
        cropped_names = filter(isCropfaceFilename, dirList) # only keep image files
        return cropped_names

    def __findMaxSize(self):
        """
            Face images are rectangles, find the maximum rectangle size
        """
        max_width = -1
        #max_ratio # height/width ratio
        cropped_files = self.getCroppedFaceImages()
        for fname in cropped_files:
            # cropped faces images have the following filename-format [0-9]*4_cropface_[0-9]*4.jpg
            print fname
            image_location = self.cropped_faces_dir + "\\" + fname
            image = highgui.cvLoadImage(image_location, 1) # a cropped non-normalized image

            print "width: " + str(image.width)
            print "height: " + str(image.height)
            ratio = image.height/image.width
            print "ratio: " + str(ratio)
            if image.width > max_width:
                max_width = image.width
        return max_width
    
    def normalizeFaces(self, useSize=True, size=None):
        """
            Normalizes all the images in the cropped_faces_dir
        """
        max_size = 0
        if size == None:
            # use default size if none
            size = DEFAULT_FACE_SIZE
            
        if useSize == False:
            # use the maximum face size found
            max_size = self.__findMaxSize()
        else:
            max_size = size
            
        # loop over the original images
        cropped_files = self.getCroppedFaceImages()
        self.filecount = len(cropped_files)

        if self.startCallback is not None:
            self.startCallback(self.filecount)
            
        print "Normalizing " + str(self.filecount) + " images"
        for index, fname in enumerate(cropped_files):
            image_location = self.cropped_faces_dir + "\\" + fname

            image = highgui.cvLoadImage(image_location, 1) # a cropped non-normalized image
            p = re.compile(CROPFACE_FILENAME_PATTERN)
            m = p.match(fname)
            prefix = m.group("prefix")
            image_index = m.group("image_index")
            face_index = m.group("face_index")
            
            norm_image = self.__normImage(image, max_size) # normalize the image

            norm_filename = prefix + "_" + image_index + "_norm_" + face_index + ".jpg"
            location = self.norm_dir + "\\" + norm_filename
            highgui.cvSaveImage(location, norm_image) # save the image to file
            
            if self.iterCallback is not None:
                self.iterCallback(index)

            

    def __normImage(self, img, length):
        #print "Generating norm image..."
        width = length
        height = length
        gray = cv.cvCreateImage(cv.cvSize(img.width,img.height), 8, 1);
        small_img = cv.cvCreateImage(cv.cvSize(cv.cvRound(width),
                                           cv.cvRound(height)), 8, 1 );
    
        # convert color input image to grayscale
        cv.cvCvtColor(img, gray, cv.CV_BGR2GRAY);
        # scale input image for faster processing
        cv.cvResize(gray, small_img, cv.CV_INTER_LINEAR);
        cv.cvEqualizeHist(small_img, small_img);
        #cvClearMemStorage(self.storage);
        norm_image = small_img # save the 'normalized image'
        return norm_image
            

class ImageResizer:
    
    def __init__(self):
        pass
    
    def resizeImages(self, image_locations, size):
        """
            resizes the images to a rectangle with the given size
        """
        for image_location in image_locations:
            # resize this image
            pass
        
    def resizeImage(self, image_location, ouput_location, size):
        """
            resizes the image to a rectangle with the given size and saves it
        """
        width = size
        height = size
        
        input_image = highgui.cvLoadImage(image_location, 1) # flag: >0 the loaded image is forced to be a 3-channel color image
        
        output_image = cv.cvCreateImage(cv.cvSize(cv.cvRound(width), cv.cvRound(height)), 8, 3);
        cv.cvResize(input_image, output_image, cv.CV_INTER_LINEAR);
        highgui.cvSaveImage(ouput_location, output_image) # save the image to file
        
if __name__ == "__main__":
    print "run main"
    resizer = ImageResizer()
    size = 200
    image_location = GALLERY_LOCATION + "\\cropped\\BARL\\BARL_0001_cropface_0000.jpg"
    ouput_location = GALLERY_LOCATION + "\\norm\\BARL\\BARL_0001_norm_0000.jpg"
    #image_location = GALLERY_LOCATION + "\\test\\sample_dennis\\ZAS1_0000_norm_0000.jpg"
    crop = GALLERY_CROPPED
    print crop
    print image_location
    #ouput_location = GALLERY_LOCATION + "\\test\\sample_dennis\\ZAS1_0000_norm_0000.jpg"
    resizer.resizeImage(image_location, ouput_location, size)
    print isCropfaceFilename(ouput_location)
    norma = FaceNormalizer("BARL")
    norma.normalizeFaces()
