import os
import re
import shutil
from marleendetector.image_util import *
#from marleendetector.normalizer import *

GALLERY_LOCATION = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\PTG\\workspace\\MarleenDetector\\gallery"
GALLERY_LIBRARY = GALLERY_LOCATION + "\\library"
GALLERY_CROPPED = GALLERY_LOCATION + "\\cropped"
GALLERY_NORM = GALLERY_LOCATION + "\\norm"

GALLERY_EYES = GALLERY_LOCATION + "\\eyes"

GALLERY_PERSONS = GALLERY_LOCATION + "\\persons.txt"
GALLERY_PERSON_BINDINGS = GALLERY_LOCATION + "\\person_bindings.txt"

CROPFACE_FILENAME_PATTERN = '(?P<prefix>[a-zA-Z0-9]+)_(?P<image_index>[a-zA-Z0-9]+)_cropface_(?P<face_index>[a-zA-Z0-9]+)[.]jpg$'
NORMFACE_FILENAME_PATTERN = '(?P<prefix>[a-zA-Z0-9]+)_(?P<image_index>[a-zA-Z0-9]+)_norm_(?P<face_index>[a-zA-Z0-9]+)[.]jpg$'

class LibraryInfo:
    def __init__(self, library_id, description):
        self.library_id = library_id
        self.description = description
        
    def __str__(self):
        short_description = description[0:200]
        return "<Library library_id:%s, descr:%s>" % (self.library_id, short_description)

class GalleryManager:
    """
    Gallery Manager handles loading and saving of the images in the gallery.
    A Gallery contains normalized images, each person has its own folder.
    """ 
    
    def __init__(self):
        pass
    
    def getPersonImages(self, person_name):
        """
            person_id is a string
            Returns a list of images of the specified person
        """
        person_dir = GALLERY_LOCATION + "\\" + person_name
        dirList = os.listdir(person_dir) # all files in the dir
        return map(lambda x: person_dir + "\\" + x, dirList)

    def getLibrary(self, prefix):
        """
            returns the folder name of the library with the specified prefix
        """
        return GALLERY_LIBRARY + "\\" + prefix
    
    def moveFacesToPersonDir(self, bindings):
        """
            Copies the faces to GALLERY_LOCATION\$person_name
        """
        for person_name in bindings:
            self.copyImagesToPerson(person_name, bindings[person_name])
    
    def copyImagesToPerson(self, person_name, image_filenames):
        return map(lambda x: self.copyImageToPerson(person_name, x), image_filenames)
        
    def copyImageToPerson(self, person_name, image_filename):
        """
        Checks if the directory GALLERY_LOCATION\$(person_name.lower()) exists (if not create it) and copy image to the dir
        @param image_filename: should exist in GALLERY_NORM
        @type image_filename: string
        @param person_name: the name of the person
        @type person_name: string
        """
        path_name = GALLERY_LOCATION + "\\" + person_name.lower()
        if os.path.isdir(path_name):
            # dir exists
            pass
        else:
            # dir does not exist, create it
            os.mkdir(path_name)
        pass
        src = GALLERY_NORM + "\\" + image_filename
        dst = path_name + "\\" + image_filename
        shutil.copyfile(src, dst)
        return True
    
    
    def checkPersonImageSizes(self, person_name, image_size):
        """
            returns true if all the images have the same size as image_size
        """
        images_list = self.getPersonImages(person_name)
        incorrectImages = []
        for image_location in images_list:
            dimension = getDimension(image_location)
            width, height = dimension
            if width == image_size and height == image_size:
                # image has the correct size
                pass
            else:
                incorrectImages.append(image_location)
        return incorrectImages

    def emptyDir(self, person_name):
        """
            Removes all the images in the person's dir
        """
        dir = GALLERY_LOCATION + "\\" + person_name
    

def isNormfaceFilename(filename):
    """
        Returns True if the filename matches the 
    """
    p = re.compile(NORMFACE_FILENAME_PATTERN)
    m = p.match(filename)
    if m is None:
        return False
    else:
        return True    
    
def isCropfaceFilename(filename):
    """
        returns true if filename matches the regular expression
    """
    p = re.compile(CROPFACE_FILENAME_PATTERN)
    m = p.match(filename)
    if m is None:
        return False
    else:
        return True

def getCroppedFaceImages(cropped_faces_dir=GALLERY_CROPPED):
    dirList = os.listdir(cropped_faces_dir) # all files in the dir
    cropped_names = filter(isCropfaceFilename, dirList) # only keep image files
    return cropped_names

def getNormFaceImages(norm_faces_dir=GALLERY_NORM):
    dirList = os.listdir(norm_faces_dir) # all files in the dir
    norm_names = filter(isNormfaceFilename, dirList) # only keep image files
    return norm_names

if __name__ == "__main__":
    g =  getCroppedFaceImages().__iter__()
    print g.next()
    print getCroppedFaceImages()
    print getNormFaceImages()
    galleryManager =  GalleryManager()
    print galleryManager.getPersonImages("dennis")
    print "checkPersonImageSizes"
    print len(galleryManager.checkPersonImageSizes("cropped", 400))
    print "CROP dir"
    print GALLERY_CROPPED