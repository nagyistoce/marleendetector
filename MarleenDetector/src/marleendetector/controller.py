import logging

from marleendetector.fetcher import *
from marleendetector.detectmanager import *
from marleendetector.gallerymanager import *
from marleendetector.normalizer import *

class Controller:
    
    def __init__(self):
        #
        pass
    
    # fetch images
    def __fetchImages(self, address, prefix, start, end, fetch=True):
        """
            Returns a list of image locations using a %-formatted url and range defined by start to end+1
            
            @param address: address is a %-formatted string, it will be used to generate a list of URLs ranging from start to end+1
                e.g.: http://myholiday.mysite.com/pictures/img_%04d.jpg
            @type address: %-formatted String with only one %-item which should be a decimal
            @param prefix: a prefix to distinguish between different image sources
            @type prefix: string
            @param start: the first number of the range
            @type start: integer
            @param end: the last number of the range
            @type end: integer
            @param fetch: if true, (re)-download all the images in the url-range
            
        """
        #address = "http://zellamsee.boereburg.nl/ZellamSee2008stapcamerafotos/stamcamera_0001.jpg"
        #address = "http://zellamsee.boereburg.nl/ZellamSee2008stapcamerafotos/stamcamera_%04d.jpg"
        fetcher = ImageFetcher(address, prefix, start, end)
        if fetch:
            image_list = fetcher.fetchImages()
        else:
            image_list = fetcher.getOutputImages()
        return image_list
    
    def __extractFaces(self, image_location, id):
        try:
            man = FaceDetectorManager(image_location, id)
            man.startDetection()
            #man.getFaces()
            calc_super_face=False # return all the face boxes (faces will be detected multiple times with different classifiers)
            man.getFaces(super_faces=calc_super_face) 
            man.saveFacesToFile(super_faces=calc_super_face)
            #man.showResult()
        except:
            print "Exception while detecting images! Skipping image..."
    
    def main(self, fetchData):
        address, start, end, prefix = fetchData
        print "Fetching images..."
        #downloadImages = True # download all the images
        downloadImages = False # only use this when the images are already downloaded
        image_list = self.__fetchImages(address, prefix, start, end, fetch=downloadImages) # saves the images in GALLERY_LIBRARY
        print "Done fetching images..."
        
        print "Extracting faces..." # saves the faces in GALLERY_CROPPED
        for index, image_location in enumerate(image_list):
            id = "%04d" % (index, )
            print image_location
            self.__extractFaces(image_location, prefix + "_" + id)
        print "Done extracting faces..."
        
        print "Normalizing faces..." # save normalized faces in GALLERY_NORM
        normalizer = FaceNormalizer()
        normalizer.normalizeFaces()
        print "Done normalizing faces..."
    
if __name__ == "__main__":
    # run main program
    controller = Controller()
    # %-formatted url, only one format variable is allowed
    address = "http://www.boereburg.nl/BZBALLEREMMENLOS/bzb23012009_%03d.jpg"
    #address = "http://zellamsee.boereburg.nl/ZellamSee2008stapcamerafotos/stamcamera_%04d.jpg"
    
    start = 0 # images-url range should start with this number
    end = 20 # last number of the images-url range
    prefix = "BARL" # unique prefix for this photo-set
    fetchData = (address, start, end, prefix)
    controller.main(fetchData)
