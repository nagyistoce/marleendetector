'''
Created on 3 apr 2009

@author: rlindeman
'''

class Face:

    def __init__(self, id, local_image_id, face_image_id, ul_x, ul_y, dr_x, dr_y):
        """
            Creates a Face object
        """
        self.id = id # auto generated id
        self.local_image_id = local_image_id # string
        self.face_image_id = face_image_id # int
        self.ul_x = ul_x
        self.ul_y = ul_y
        self.dr_x = dr_x
        self.dr_y = dr_y
        
    def __str__(self):
        return "Face ul_x=%s, ul_y=%s, dr_x=%s, dr_y=%s" % (self.ul_x, self.ul_y, self.dr_x, self.dr_y)