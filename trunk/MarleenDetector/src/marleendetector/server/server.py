import pprint
import sys, traceback
from cgi import parse_qs, escape

from marleendetector.faces.faceorigins import *
from marleendetector.server.generator.ImageHTML import *
from marleendetector.server.generator.ImageListHTML import *

class MDServerApp:
    """
    MarleenDetectorServerApp
    
    (Note: 'MDServerApp' is the "application" here, so calling it
    returns an instance of 'AppClass', which is then the iterable
    return value of the "application callable" as required by
    the spec.

    If we wanted to use *instances* of 'AppClass' as application
    objects instead, we would have to implement a '__call__'
    method, which would be invoked to execute the application,
    and we would need to create an instance for use by the
    server or gateway.
    
    """
    FILE = 'frontend.html'


    def __init__(self, environ, start_response):
        print "start"
        self.environ = environ
        self.start_response = start_response
        self.database = FaceOriginsDB()

    def __iter__(self):
        #pprint.pprint(environ)
        #print start_response
        print "REQ_METHOD:" + str(self.environ['REQUEST_METHOD'])
        
        d = None
        try:
            request_body_size = int(self.environ['CONTENT_LENGTH'])
            request_body = self.environ['wsgi.input'].read(request_body_size)
            d = parse_qs(request_body)
            print "data:" + str(d)
        except (TypeError, ValueError), e:
            traceback.print_exc(file=sys.stdout)
            request_body = "0"        
        if self.environ['REQUEST_METHOD'] == 'POST':

            try:
                local_image_id = d.get('image_id', [''])[0]
                faces = self.database.getFaceData(local_image_id)
                imageOrigin = self.database.getImageOrigin(local_image_id)
                #print "body" + str(len(faces))
                responseHTML = ImageHTML(imageOrigin, faces)
                response_body = str(responseHTML.getResponse())
                #print "body: " + str(response_body)
            except Exception, e:
                traceback.print_exc(file=sys.stdout)
                response_body = "<b>error</b>"
            status = '200 OK'
            headers = [('Content-type', 'text/html'),
                       ('Content-Length', str(len(response_body)))]
            self.start_response(status, headers)
            yield response_body
        else:
            responseHTML = ImageListHTML()
            #response_body = str(responseHTML.getResponse())
            response_body = open(MDServerApp.FILE).read()
            status = '200 OK'
            headers = [('Content-type', 'text/html'),
                       ('Content-Length', str(len(response_body)))]
            self.start_response(status, headers)
            yield response_body
