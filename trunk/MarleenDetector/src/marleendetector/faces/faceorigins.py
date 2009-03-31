'''
Created on 31 mrt 2009

            # faces_data = [face_data, face_data, ...]
            # face_data = (org_image_id, face_image_id, face_rectangle)
            
@author: rlindeman
'''
from pysqlite2 import dbapi2 as sqlite

class FaceOriginsDB:
    
    def __init__(self):
        self.connection = sqlite.connect('faces.db')
        self.cursor = connection.cursor()
        # Check  if table exists
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="FaceData" ORDER BY name;')
        tables = cursor.fetchall()
        if (len(tables)):
            print "Table 'FaceData' not found, create it!"
            self.cursor.execute('CREATE TABLE FaceData (id INTEGER PRIMARY KEY, org_image_id VARCHAR, face_image_id INTEGER, ul.x INTEGER, ul.y INTEGER, dr.x INTEGER, dr.y INTEGER)')

    def addFaceData(self, face_data):
        # values_tuple ('BARL_0001', 0, (cvPoint(341,159), cvPoint(449,267)))
        (org_image_id, face_image_id, face_rectangle) = face_data
        (ul, dr) = face_rectangle
        values_tuple = (org_image_id, face_image_id, ul.x, ul.y, dr.x, dr.y)
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
