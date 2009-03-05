# normalizes the extracted faces and resizes them
import os
import re

from opencv.cv import *
from opencv.highgui import *

from marleendetector.gallerymanager import *



NORM_FILENAME = "norm_%04d.jpg"
DEFAULT_FACE_SIZE = 400


class FaceNormalizer:
    
    def __init__(self, cropped_faces_dir=GALLERY_CROPPED, norm_dir=GALLERY_NORM):
        self.cropped_faces_dir = cropped_faces_dir # non normalized faces location
        self.norm_dir = norm_dir # normalized faces dir
        pass
    
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
            image = cvLoadImage(image_location, 1) # a cropped non-normalized image

            print "width: " + str(image.width)
            print "height: " + str(image.height)
            ratio = image.height/image.width
            print "ratio: " + str(ratio)
            if image.width > max_width:
                max_width = image.width
        return max_width
    
    def normalizeFaces(self, useDefaultSize=True):
        max_size = DEFAULT_FACE_SIZE
        if useDefaultSize == False:
            # use the maximum face size found
            max_size = self.__findMaxSize()
            
        # loop over the original images
        cropped_files = self.getCroppedFaceImages()
        for index, fname in enumerate(cropped_files):
            image_location = self.cropped_faces_dir + "\\" + fname
            image = cvLoadImage(image_location, 1) # a cropped non-normalized image
    
            p = re.compile(CROPFACE_FILENAME_PATTERN)
            m = p.match(fname)
            prefix = m.group("prefix")
            image_index = m.group("image_index")
            face_index = m.group("face_index")
            
            norm_image = self.__normImage(image, max_size) # normalize the image

            norm_filename = prefix + "_" + image_index + "_norm_" + face_index + ".jpg"
            location = self.norm_dir + "\\" + norm_filename
            cvSaveImage(location, norm_image) # save the image to file

    def __normImage(self, img, length):
        print "Generating norm image..."
        width = length
        height = length
        gray = cvCreateImage(cvSize(img.width,img.height), 8, 1);
        small_img = cvCreateImage(cvSize(cvRound(width),
                                           cvRound(height)), 8, 1 );
    
        # convert color input image to grayscale
        cvCvtColor(img, gray, CV_BGR2GRAY);
        # scale input image for faster processing
        cvResize(gray, small_img, CV_INTER_LINEAR);
        cvEqualizeHist(small_img, small_img);
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
        
        input_image = cvLoadImage(image_location, 1) # flag: >0 the loaded image is forced to be a 3-channel color image
        
        output_image = cvCreateImage(cvSize(cvRound(width), cvRound(height)), 8, 3);
        cvResize(input_image, output_image, CV_INTER_LINEAR);
        cvSaveImage(ouput_location, output_image) # save the image to file
        
if __name__ == "__main__":
    print "run main"
    resizer = ImageResizer()
    size = 200
    image_location = GALLERY_LOCATION + "\\test\\sample_dennis\\ZAS1_0000_norm_0000.jpg"
    crop = GALLERY_CROPPED
    print crop
    print image_location
    ouput_location = GALLERY_LOCATION + "\\test\\sample_dennis\\ZAS1_0000_norm_0000.jpg"
    resizer.resizeImage(image_location, ouput_location, size)
    print isCropfaceFilename(ouput_location)
    
