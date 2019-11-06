#!/usr/bin/python
import mimetypes
import os
import zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer

from config import Config
from lib.library import Catalogue
from lib.storage import Storage

config = Config()
Storage = Storage()


class InitFiles:
    """First run file creation operations"""
    def __init__(self, file_array):
        print("Begining creation of file structure")
        for _pointer in file_array:
            if not os.path.isfile(_pointer):
                self.CreateFile(_pointer)
        print("Concluded file creation")

    def CreateFile(self, _pointer):
        """Create the file"""
        if not os.path.isdir(os.path.split(_pointer)[0]):
            os.mkdir(os.path.split(_pointer)[0])
            f = open(_pointer, "w+")
        f.close()


class RequestHandler(BaseHTTPRequestHandler):
    """Request Handler"""
    def do_GET(self):
        # TODO determine how to include stylesheets
        self.send_response(200)
        if self.path == '/':
            self.path = '../static/index.html'
            mimetype = 'text/html'
            serve_file = open(self.path[1:]).read()
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(bytes(serve_file, 'utf-8'))
        elif self.path.split('.', 1)[1] == 'css':
            self.path = '../static' + self.path
            mimetype = 'text/css'
            serve_file = open(self.path[1:]).read()
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(bytes(serve_file, 'utf-8'))
        elif self.path.endswith('.png'):
            self.path = '../static' + self.path
            mimetype = 'image/png'
            serve_file = open(self.path[1:], 'rb') # Important to rb read binary for images
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(serve_file.read())
        else:
            self.send_response(404)
            serve_file = "File Not Found"
            mimetype = 'text/html'
            self.send_header('Content-type', mimetype)
            self.end_headers()
        try: serve_file.close()
        except Exception: pass

class BookServer:
    """HTTP Frontend"""
    def __init__(self):
        # TODO Get server Ip Address
        self.server_address = ('', 8000)
        self.handler = RequestHandler

    def close_prompt(self):
        """Prompt to close server"""
        close = input("Close Server? y/n")
        if close == 'y':
            self.close()
            return True
        else:
            self.close_prompt()

    def run(self):
        """Start HTTP Server"""
        self.httpd = HTTPServer(self.server_address, self.handler)
        try:
            print("Server running @ http://127.0.0.1:8000")
            self.httpd.serve_forever()
            self.httpd.handle_request()
        except KeyboardInterrupt:
            print("Interrupt received, Closing Server")
            self.close()
            print("Server shutdown, Goodbye!")
            return False

    def close(self):
        """Stop HTTP Server"""
        try:
            self.httpd.server_close()
            return True
        except Exception:
            return False
