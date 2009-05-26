import marleendetector.database.dbconnection as dbconnection
import numpy

class Rectangle:
    
    def __init__(self, ul_x, ul_y, dr_x, dr_y):
        if (ul_x > dr_x):
            # swap x values...
            temp = ul_x
            ul_x = dr_x
            dr_x = temp
        if (ul_y < dr_y):
            # swap y values...
            temp = ul_y
            ul_y = dr_y
            dr_y = temp
        if not (ul_x < dr_x and ul_y > dr_y):
            raise ValueError("Up left should really be the upper left corner. ul_x(%s) < dr_x(%s) and ul_y(%s) > dr_y(%s)" % (ul_x, dr_x, ul_y, dr_y));
        self.ul_x = ul_x
        self.ul_y = ul_y
        self.dr_x = dr_x
        self.dr_y = dr_y
        
    def width(self):
        return self.dr_x - self.ul_x
    
    def height(self):
        return self.ul_y - self.dr_y
        
    def size(self):
        return self.height() * self.width()
    
    def overLapsWith(self, rectangle):
        #print "%s < %s and %s > %s and %s > %s and %s < %s" % (self.ul_x, rectangle.dr_x, self.dr_x, rectangle.ul_x, self.ul_y, rectangle.dr_y, self.dr_y, rectangle.ul_y)
        return self.ul_x < rectangle.dr_x and self.dr_x > rectangle.ul_x and self.ul_y > rectangle.dr_y and self.dr_y < rectangle.ul_y


    def overLapRectange(self, rectangle):
        """
            returns the Rectangle that defines the overlap
        """
        if not self.overLapsWith(rectangle):
            return Rectangle(0, 0, 0, 0)
        else:
            x_min = min(self.dr_x, rectangle.dr_x)
            x_max = max(self.ul_x, rectangle.ul_x)
            y_min = min(self.ul_y, rectangle.ul_y)
            y_max = max(self.dr_y, rectangle.dr_y)
            #return Rectangle(ul_x, ul_y, dr_x, dr_y)
            return Rectangle(x_min, y_max, x_max, y_min)
        
    def overLapSize(self, rectangle):
        """
        Returns the size of the overlap area of the rectangles
        """
        if not self.overLapsWith(rectangle):
            return 0
        else:
            x_overlap = min(self.dr_x, rectangle.dr_x) - max(self.ul_x, rectangle.ul_x)
            y_overlap = min(self.ul_y, rectangle.ul_y) - max(self.dr_y, rectangle.dr_y)
            overlap = x_overlap * y_overlap          
            return overlap
        
    def overlapPercentage(self, rectangle):
        overlap = self.overLapSize(rectangle)
        sumsize = self.size() + rectangle.size() - overlap
        per = (float(overlap) / float(sumsize)) * 100
        return per
        
THRESHOLD_OVERLAP = 60

class Cluster:
    
    def __init__(self):
        self.items = []
        
    def checkOverlap(self, rectangle):
        return map(rectangle.overlapPercentage, self.items)
            
    def inCluster(self, rectangle):
        belowThreshold = filter(lambda x: x < THRESHOLD_OVERLAP, self.checkOverlap(rectangle))
        minAreaPercentage = min(self.checkOverlap(rectangle))
        return (len(belowThreshold) == 0, minAreaPercentage)
        
    def __str__(self):
        
        return "<Cluster size=%s>" % (len(self.items), )
def clusterRectangles(rectangles):
    """
        If rectangles overlap above a certain threshold they are placed in the same cluster
        otherwise a new cluster is created
    """
    clusters = []
    for rectangle in rectangles:
        if len(clusters) == 0:
            # no cluster, create cluster
            cluster = Cluster()
            cluster.items.append(rectangle)
            clusters.append(cluster)
        else:
            # find a cluster with rectangles that have an overlap area above threshold
            overlaps = zip(map(lambda x: x.inCluster(rectangle), clusters), clusters)
            if len(filter(lambda x: x[0][0], overlaps)) > 0:
                # add to cluster with max overlap
                maxClusterData = max(overlaps, key=lambda k: k[0][0])
                maxClusterData[1].items.append(rectangle)
            else:
                # rectangle does not fit in another cluster, create a new one
                cluster = Cluster()
                cluster.items.append(rectangle)
                clusters.append(cluster)                
            #print overlaps
    return clusters
         
def getRectangleFromFace(face):
    """
        Converts a Face to a Rectangle
    """
    return Rectangle(face.ul_x, face.ul_y, face.dr_x, face.dr_y)
    

def generate_super_rectangle(rec_list):
    """
    generate the smallest rectangle in which al rectangles will fit
    """
    lu_x = -1 # upper left corner, x
    lu_y = -1 # upper left corner, y
    rd_x = -1 # down right corner, x
    rd_y = -1 # down right corner, y
    for rec in rec_list:
        r_lu, r_rd = rec
        # upper left corner
        if lu_x == -1 or r_lu.x < lu_x:
            lu_x = r_lu.x
        if lu_y == -1 or r_lu.y < lu_y:
            lu_y = r_lu.y
        # down right corner
        if rd_x == -1 or r_rd.x > rd_x:
            rd_x = r_rd.x
        if rd_y == -1 or r_rd.y > rd_y:
            rd_y = r_rd.y
    return (cvPoint(lu_x,lu_y), cvPoint(rd_x,rd_y))

def listsAreTheSame(list_a, list_b):
    return set(list_a).issubset(set(list_b)) 

def rectanglesOverlap(rec1, rec2):
    r1_lu, r1_rd = rec1
    r2_lu, r2_rd = rec2
    return r1_lu.x < r2_rd.x and r1_rd.x > r2_lu.x and r1_lu.y < r2_rd.y and r1_rd.y > r2_lu.y    

# calculate the overlapping rectangles lists
def get_overlappingrectangles(rectangle, rectangle_list):
    r1_lu, r1_rd = rectangle
    overlaps = []
    for rec_tuple in rectangle_list:
        r2_lu, r2_rd = rec_tuple
        if rectanglesOverlap(rectangle, rec_tuple):
            pass
            #print "overlap " + str(rec_tuple)
            overlaps.append(rec_tuple)
        else:
            pass
            #print "no overlap"
    return overlaps


# generate bitmap of rectangles, the higher the number, more rectangles
def generateBitMap(rectangle_list):
    M = height
    N = width
    A = numpy.matrix(numpy.zeros((M,N), dtype=int))
    for rec_tuple in rectangle_list:
        lu, rd = rec_tuple
        list_x = range(lu.x, rd.x) # height
        list_y = range(lu.y, rd.y) # width
        for x in list_x:
            for y in list_y:
                A[x, y] = A[x, y] + 1
    # draw point
    for x in range(0, height-1):
        for y in range(0, width-1):
            point = A[x, y]
            if point > 0:
                # draw point
                pt = cvPoint(x, y)
                base_c = 100
                radi = (255-100)/8 * point
                v = base_c + radi
                cvCircle(detect.output_image, pt, 2, CV_RGB(v,v,v), -1)
    print "circle done"


if __name__ == "__main__":
    print "Main"
    db = dbconnection.DBConnection()
    rows = db.executeQuery("SELECT local_image_id FROM FaceData GROUP BY local_image_id HAVING COUNT(*) > 1");
    for row in rows:
        #query = "SELECT * FROM FaceData WHERE local_image_id = %s" % row
        #print query
        print str(row)
        images = db.executePQuery("SELECT * FROM FaceData WHERE local_image_id = ?", row);
        print images
        for image in images:
            id, local_image_id, face_image_id, ul_x, ul_y, dr_x, dr_y = image
