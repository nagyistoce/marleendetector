# Controller
# main-method:
# 1. Download a sequence of pictures from the web
# 2. Detect faces in these images
# 3. Normalize the face-images
import logging

from marleendetector.fetcher import *
from marleendetector.detectmanager import *
from marleendetector.gallerymanager import *
from marleendetector.normalizer import *
from marleendetector.faces.faceorigins import *

class Controller:
    
    def __init__(self, downloadImages=False):
        """
            Initializes the Controller. The Controller downloads images, detects faces,
            saves the faces to file and normalizes the images
            
            @param downloadImages: if downloadImages is True the images will be (re)downloaded from the web,
                                   if False the images are presumed to be already saved on disk in the library dir
        """
        self.downloadImages = downloadImages
        self.gallerymanager = GalleryManager()
        self.facedataDB = FaceOriginsDB()
        print "Done creating"
    
    # fetch images
    def __fetchImages(self, address, prefix, start, end, fetch=True):
        """
            Returns a list of image locations using a %-formatted url and range defined by start to end+1
            returns [(index, org_image_name, local_image_id, local_path), ...]
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
        fetcher = ImageFetcher(address, prefix, start, end, output_dir=self.gallerymanager.getLibrary(prefix))
        if fetch:
            image_list = fetcher.fetchImages() # redownload the images
        else:
            image_list = fetcher.getOutputImages() # generate the filename list
        return image_list
    
    def __extractFaces(self, image_location, prefix, id):
        """
            Detect faces in the image and save them separately
            image_location is the location of the image file on disk
            prefix is the name of this image collection
            id is the unique name of this image
        """
        try:
            man = FaceDetectorManager(image_location, prefix, id)
            man.startDetection()
            #man.getFaces()
            calc_super_face=False # return all the face boxes (faces will be detected multiple times with different classifiers)
            man.getFaces(super_faces=calc_super_face) 
            faces_data = man.saveFacesToFile(super_faces=calc_super_face)
            # faces_data = [face_data, face_data, ...]
            # face_data = (org_image_id, face_image_id, face_rectangle)
            #man.showResult()
            return faces_data
        except Exception, inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
            print "Exception while detecting images! Skipping image..."
    
    def main(self, fetchData):
        """
            1. Download a sequence of pictures from the web and returns a list with image file_locations
            2. Detect faces in these images
            3. Normalize the face-images
        """
        address, start, end, prefix = fetchData
        print "Fetching images..."
        downloadImages = self.downloadImages # only use this when the images are already downloaded
        image_list = self.__fetchImages(address, prefix, start, end, fetch=downloadImages) # saves the images in GALLERY_LIBRARY
        # image_list = [(image_url, filename, filepath), ... ]
        print "Done fetching images..."
        for index, org_image_name, local_image_id, local_path in image_list:
            self.facedataDB.addImageOrigin(org_image_name, local_image_id, local_path)
            
        all_face_data = []
        print "Extracting faces..." # saves the faces in GALLERY_CROPPED
        for index, image_url, filename, filepath in image_list:
            id = "%04d" % (index, )
            print filepath
            faces_data = self.__extractFaces(filepath, prefix, prefix + "_" + id)
            # faces_data = [face_data, face_data, ...]
            # face_data = (org_image_id, face_image_id, face_rectangle)
            if faces_data is not None:
                all_face_data.extend(faces_data)     
        print "Done extracting faces..."
        print all_face_data
        for face_data in all_face_data:
            (org_image_id, face_image_id, face_rectangle) = face_data
            (ul, dr) = face_rectangle
            self.facedataDB.addFaceData(face_data)
        #return
        print "Normalizing faces..." # save normalized faces in GALLERY_NORM
        normalizer = FaceNormalizer(prefix)
        normalizer.normalizeFaces()
        print "Done normalizing faces..."
    
if __name__ == "__main__":
    # run main program
    controller = Controller()
    controller.downloadImages = True # download the images
    # %-formatted url, only one format variable is allowed
    address = "http://www.boereburg.nl/BZBALLEREMMENLOS/bzb23012009_%03d.jpg"
    #address = "http://zellamsee.boereburg.nl/ZellamSee2008stapcamerafotos/stamcamera_%04d.jpg"
    
    start = 0 # images-url range should start with this number
    end = 100 # last number of the images-url range
    prefix = "BARL" # unique prefix for this photo-set
    fetchData = (address, start, end, prefix)
    controller.main(fetchData)
