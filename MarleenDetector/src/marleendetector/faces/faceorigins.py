'''
Created on 31 mrt 2009

            # faces_data = [face_data, face_data, ...]
            # face_data = (org_image_id, face_image_id, face_rectangle)
            
@author: rlindeman
'''
from pysqlite2 import dbapi2 as sqlite

from marleendetector.gallerymanager import *
from marleendetector.faces.face import *



class FaceOriginsDB:
    
    def __init__(self):
        """
        Creates a FaceData table
        """
        db_location = GALLERY_DATABASE + "\\faces.db"
        self.connection = sqlite.connect(db_location)
        self.cursor = self.connection.cursor()
        # init tables
        self.__initTables()

    def __initTables(self):
        """
            Creates tables when they don't exist
        """
        # Check FaceData table
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="FaceData" ORDER BY name;')
        tables = self.cursor.fetchall()
        if (len(tables) == 0):
            print "Table 'FaceData' not found, create it!"
            self.__createFaceDataTable()
        # Check ImageOrigin table
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="ImageOrigin" ORDER BY name;')
        tables = self.cursor.fetchall()
        if (len(tables) == 0):
            print "Table 'ImageOrigin' not found, create it!"
            self.__createImageOriginTable()

    def __createImageOriginTable(self):
        """
            Creates the ImageOrigin table
        """
        self.cursor.execute('CREATE TABLE ImageOrigin (id INTEGER PRIMARY KEY, org_image_name VARCHAR, local_image_id VARCHAR, local_path VARCHAR)')
        self.connection.commit()
            
    def __createFaceDataTable(self):
        """
            Creates the FaceData table
        """
        self.cursor.execute('CREATE TABLE FaceData (id INTEGER PRIMARY KEY, local_image_id VARCHAR, face_image_id INTEGER, ul_x INTEGER, ul_y INTEGER, dr_x INTEGER, dr_y INTEGER)')
        self.connection.commit()



    def getFaceData(self, local_image_id):
        """
            Returns a list of Face-objects
        """
        print "getFaceData: " + str(local_image_id)
        #local_image_id = "BARL_0001"
        self.cursor.execute('SELECT * FROM FaceData WHERE local_image_id = ?', (str(local_image_id),))
        faces = []
        for row in self.cursor:
            face = Face(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            faces.append(face)
        return faces
    
    def getImageOrigin(self, local_image_id):
        """
            Returns an Image Origin Row
            tuple(id, org_image_name, local_image_id, local_path)
        """
        local_image_id = local_image_id + ".jpg"
        self.cursor.execute("SELECT * FROM ImageOrigin WHERE local_image_id = ?", (local_image_id,))
        row = self.cursor.fetchone()
        return row
    
    def addImageOrigin(self, org_image_name, local_image_id, local_path):
        values_tuple = (org_image_name, local_image_id, local_path)
        self.cursor.execute('INSERT INTO ImageOrigin VALUES (NULL, ?, ?, ?)', values_tuple)
        # Save (commit) the changes
        self.connection.commit()        
        
                
    def addFaceData(self, face_data):
        """
        add the face_data to the database
        face_data = ('BARL_0001', 0, (cvPoint(341,159), cvPoint(449,267)))
        """
        # values_tuple ('BARL_0001', 0, (cvPoint(341,159), cvPoint(449,267)))
        (local_image_id, face_image_id, face_rectangle) = face_data
        (ul, dr) = face_rectangle
        values_tuple = (local_image_id, face_image_id, ul.x, ul.y, dr.x, dr.y)
        self.cursor.execute('INSERT INTO FaceData VALUES (NULL, ?, ?, ?, ?, ?, ?)', values_tuple)
        # Save (commit) the changes
        self.connection.commit()        

    def close(self):
        """
            Close the database connection
        """
        # We can also close the cursor if we are done with it
        self.cursor.close()
        self.connection.close()        
