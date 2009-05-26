'''
Created on 26 mei 2009

@author: rlindeman
'''

# import the necessary things for OpenCV
from opencv import cv
#from opencv import highgui

# for making random numbers
from random import Random

colour = {}
colour["red"] = cv.CV_RGB(255,0,0)
colour["green"] = cv.CV_RGB(0,255,0)
colour["blue"] = cv.CV_RGB(0,0,255)
colour["yellow"] = cv.CV_RGB(0,255,255)
colour["asd"] = cv.CV_RGB(255,0,255)
colour["ert"] = cv.CV_RGB(255,255,0)
colour["yujyuj"] = cv.CV_RGB(50,255,0)
colour["kgsd"] = cv.CV_RGB(100,5,200)
colour["sdcjr"] = cv.CV_RGB(5,100,200)
colour["qqwer"] = cv.CV_RGB(5,5,100)

color_iter = colour.itervalues()

def random_color (random):
    """
    Return a random color
    """
    icolor = random.randint (0, 0xFFFFFF)
    return cv.cvScalar (icolor & 0xff, (icolor >> 8) & 0xff, (icolor >> 16) & 0xff)

    
if __name__ == "__main__":
    print "main"
    print color_iter.next()
    print color_iter.next()