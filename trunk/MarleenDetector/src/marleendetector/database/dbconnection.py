from pysqlite2 import dbapi2 as sqlite

from marleendetector.gallerymanager import *

class DBConnection:
    
    def __init__(self):        
        db_location = GALLERY_DATABASE + "\\faces.db"
        self.connection = sqlite.connect(db_location)
        self.cursor = self.connection.cursor()
        
    def executeQuery(self, query):
        """
            query is a SELECT-query
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def executePQuery(self, query, *parms):
        """
            query is a SELECT-Parameter-query
            parms is a tuple
        """
        self.cursor.execute(query, *parms)
        return self.cursor.fetchall()
          
if __name__ == "__main__":
    print "Main"
    db = DBConnection()
    rows = db.executeQuery("SELECT local_image_id FROM FaceData GROUP BY local_image_id HAVING COUNT(*) > 1");
    for row in rows:
        print row