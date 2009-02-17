import os
import re
import shutil

GALLERY_LOCATION = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\PTG\\workspace\\MarleenDetector\\gallery"
GALLERY_LIBRARY = GALLERY_LOCATION + "\\library"
GALLERY_CROPPED = GALLERY_LOCATION + "\\cropped"
GALLERY_NORM = GALLERY_LOCATION + "\\norm"

GALLERY_PERSONS = GALLERY_LOCATION + "\\persons.txt"
GALLERY_PERSON_BINDINGS = GALLERY_LOCATION + "\\person_bindings.txt"

CROPFACE_FILENAME_PATTERN = '(?P<prefix>[a-zA-Z0-9]+)_(?P<image_index>[a-zA-Z0-9]+)_cropface_(?P<face_index>[a-zA-Z0-9]+)[.]jpg$'
NORMFACE_FILENAME_PATTERN = '(?P<prefix>[a-zA-Z0-9]+)_(?P<image_index>[a-zA-Z0-9]+)_norm_(?P<face_index>[a-zA-Z0-9]+)[.]jpg$'

class GalleryManager:
    """
    Gallery Manager handles loading and saving of the images in the gallery.
    A Gallery contains normalized images, each person has its own folder.
    """ 
    
    def __init__(self):
        pass
    
    def getImages(self, person_id):
        """
            person_id is a string
            Returns a list of images of the specified person
        """
        pass
    
    def sortBindings(self, bindings):
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

if __name__ == "main":
    g =  getCroppedFaceImages().__iter__()
    print g.next()
    print getCroppedFaceImages()
    print getNormFaceImages()