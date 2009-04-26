import urllib2
import os
# fetch images from the web and save them to disk
# use regex to download a range of images

from marleendetector.gallerymanager import *

SAVED_IMAGE_PATTERN = "_%04d.jpg"

class ImageFetcher:
    def __init__(self, address, prefix, start_number, end_number, output_format=SAVED_IMAGE_PATTERN, output_dir=GALLERY_LIBRARY):
        """
            address should be a %-format string
            prefix is used to distinguish between different image sources or events
            start_number is the number the sequence will begin with
            end_number is the last number of the sequence (inclusive)
        """
        self.address = address
        self.prefix = prefix
        self.start_number = start_number
        self.end_number = end_number + 1
        self.output_format = self.prefix + output_format
        if output_dir is None:
            # output dir is not set, use the current dir
            self.output_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.output_dir = output_dir

    
    def __generateImageList(self):
        """
            generate a list of image location on the web
        """
        seq = range(self.start_number, self.end_number)
        list = map(lambda x: self.address % (x, ), seq)
        return list
    
    def getOutputImages(self):
        """
            Generate a list with file locations
        """
        output_images = []
        seq = range(self.start_number, self.end_number)
        list = map(lambda x: self.output_format % (x, ), seq)
        #filename = self.output_format % (index,)
        #filepath = os.path.join(__dir__, filename)
        output_images = map(lambda filename: os.path.join(self.output_dir, filename),list)        
        return output_images
    
    def fetchImages(self):
        """
            Images are stored in the self.output_dir dir
            Returns a list of tuples [(image_url, filename, filepath), ... ]
        """
        print "Fetching..."
        image_list = self.__generateImageList()
        output_images = [] # [(image_url, filename, filepath), ... ]

        # filename = "fetch" + str(index) + ".txt"
        for index, image_url in enumerate(image_list):
            print "Fetch " + image_url
            opener1 = urllib2.build_opener()
            page1 = None
            try:
                page1 = opener1.open(image_url)
                my_picture = page1.read() # read the image
                filename = self.output_format % (index,) # insert the current index into the image file name
                filepath = os.path.join(self.output_dir, filename)
                print filepath # we will save the file here
                output_images.append((image_url, filename, filepath))
                #db.addImageOrigin(image_url, filename, filepath)
                #output_images.append(filepath)   
                fout = open(filepath, "wb")
                fout.write(my_picture) # write the image to file
                fout.close()
            except urllib2.HTTPError, inst:
                print "HTTP Error occured at URL: " + image_url
                print inst
            except urllib2.URLError, inst:
                print "URL Error occured at URL: " + image_url
                print inst
        
        return output_images     

if __name__ == '__main__':
    #address = "http://zellamsee.boereburg.nl/ZellamSee2008stapcamerafotos/stamcamera_0001.jpg"
    address = "http://zellamsee.boereburg.nl/ZellamSee2008stapcamerafotos/stamcamera_%04d.jpg"
    prefix = "ZAS1"
    output_format = "savedimage_%04d.jpg"
    start = 0
    end = 124
    output_dir = None
    output_dir = "C:\\Documents and Settings\\rlindeman\\My Documents\\TU\\PTG\\workspace\\MarleenDetector\\gallery\\library"
    fetcher = ImageFetcher(address, prefix, start, end, output_format, output_dir=output_dir)
    image_list = fetcher.fetchImages()


    

