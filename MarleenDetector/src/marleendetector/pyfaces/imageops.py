import Image

class XImage:
    """
        This class represents an Image
    """
    
    def __init__(self, filename):
        self._readImage(filename)
        
    def _readImage(self, fname):
        """
            Opens image fname
        """
        im = Image.open(fname).convert("L") # convert to black/white image
        self._width, self._height = im.size # set the width/height
        # Convert the contents of an image to a list
        self._pixellist = [pix for pix in  im.getdata()] 

def make_image(v, filename, imsize, scaled=True):
    v.shape = (-1,)    #change to 1 dim array
    im = Image.new('L', imsize)
    if scaled:
        a, b = v.min(), v.max()    
        v = ((v - a) * 255 / (b - a))    
    im.putdata(v)    
    im.save(filename)
