'''
Created on 2 apr 2009

@author: rlindeman
'''
import threading

import webbrowser
from wsgiref.simple_server import make_server

from marleendetector.server.server import *


PORT = 8080

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, MDServerApp.FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    httpd = make_server("", PORT, MDServerApp)
    httpd.serve_forever()

if __name__ == "__main__":
    open_browser()
    start_server()