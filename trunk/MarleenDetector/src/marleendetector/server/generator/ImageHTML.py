'''
Created on 3 apr 2009

@author: rlindeman
'''
import PageHTML

class ImageHTML(PageHTML.PageHTML):


    def __init__(self, imageOrigin, faces):
        """
        imageOrigin = tuple(id, org_image_name, local_image_id, local_path)
        faces = [Face, Face, ...]
        """
        PageHTML.PageHTML.__init__(self)
        self.imageOrigin = imageOrigin
        self.faces = faces
        pass
    
    def getResponse(self):
        print "gen response"
        lines = []
        lines.extend(self.getHeader())
        content_start = """
            <div id="contents">
                <div id="imagecontainer" style="position:relative;">
                    <!-- the image -->
                    <img src="%s" />
                    <!-- all the face boxes -->
                    """
        content_face = """
                    <div class="face_box" style="border: thin solid rgb(250,0,255); width: %spx; height: %spx; position:absolute; left: %spx; top: %spx;">
                    
                    </div>
                    """
        content_end = """
                </div>
                <div>
                blablabla info...
                </div>
            </div>
        """      
        lines.append(content_start % (self.imageOrigin[1],))
        for face in self.faces:
            print "faceid: " + str(face.id)
            left = face.ul_x
            top = face.ul_y

            width = face.dr_x - face.ul_x
            print face.ul_x, face.dr_x
            
            height = face.dr_y - face.ul_y
            print face.ul_y, face.dr_y
            #print (width, height, left, top)
            lines.append(content_face % (width, height, left, top))
        lines.append(content_end)
        lines.extend(self.getFooter())
        return '\n'.join(lines)
        