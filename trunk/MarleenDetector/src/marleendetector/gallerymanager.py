import os
import re

GALLERY_LOCATION = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\PTG\\workspace\\MarleenDetector\\gallery"
GALLERY_LIBRARY = GALLERY_LOCATION + "\\library"
GALLERY_CROPPED = GALLERY_LOCATION + "\\cropped"
GALLERY_NORM = GALLERY_LOCATION + "\\norm"

GALLERY_PERSONS = GALLERY_LOCATION + "\\persons.txt"
GALLERY_PERSON_BINDINGS = GALLERY_LOCATION + "\\person_bindings.txt"


CROPFACE_FILENAME_PATTERN = '\d\d\d\d_cropface_\d\d\d\d[.]jpg$'
NORMFACE_FILENAME_PATTERN = 'norm_\d\d\d\d.jpg$'

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

g =  getCroppedFaceImages().__iter__()
print g.next()

print getCroppedFaceImages()
print getNormFaceImages()