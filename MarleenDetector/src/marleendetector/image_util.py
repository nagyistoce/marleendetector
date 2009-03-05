from opencv.highgui import *

def getDimension(image_location):
    """
        Return s the width and height of an image in a tupe
        output is: (width, height)
    """
    input_image = cvLoadImage(image_location, 1)
    width = input_image.width
    height = input_image.height
    pass
    return (width, height)

def resizeImages():
    name_list = ["arina", "dennis", "ferrie", "heidt", "jeffrey", "jeroen", "kim", "marleen", "niels", "ricky", "ronald", "sjors"]
    size = 400
    for person_name in name_list:
        incorrect = self.checkPersonImageSizes(person_name, size)
        for image_location in incorrect:
            resizer = ImageResizer()
            resizer.resizeImage(image_location, image_location, size)
    