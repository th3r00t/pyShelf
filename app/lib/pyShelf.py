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
            serve_file = open(self.path[1:], 'rb')
            # Important to rb read binary for images
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


class BookDisplay:
    """All functions related to displaying book information in the HTML UI"""

    def __init__(self):
        """
        Initialize class variables
        :return: None
        """
        self.books_per_page = None
        self.current_page = 0
        self.thumbnail_size = [200, 300]
        self.thumbnail_scale = 1
        self.total_pages = None

    def nextPage(self):
        """
        Goto next book page
        :return: new current_page
        """
        self.current_page += 1
        return self.current_page

    def previousPage(self):
        """
        Goto previous book page
        :return: new current_page
        """
        self.current_page -= 1
        return self.current_page

    def booksPerPage(self, screen_size):
        """
        Set books per page

        :param screen_size: Array containing x,y pixel sizes
        :return: self.books_per_page
        """
        x = (self.thumbnail_size[0] * self.thumbnail_scale) + 10
        y = (self.thumbnail_size[1] * self.thumbnail_scale) + 10
        self.books_per_page = int(screen_size[0]//x) * int(screen_size[1]//y)
        return self.books_per_page


class BookServer:
    """
    HTTP server functions required to display e-books
    """

    def __init__(self):
        self.server_address = ('', 8000)
        self.handler = RequestHandler
        self.httpd = HTTPServer(self.server_address, self.handler)

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
        try:
            print("Server running @ http://127.0.0.1:8000")
            self.httpd.serve_forever()
            self.httpd.handle_request()
        except KeyboardInterrupt:
            print("Interrupt received, Closing Server")
            self.close()
            print("Server shutdown, Goodbye!")
            return True

    def close(self):
        """Stop HTTP Server"""
        try:
            self.httpd.server_close()
            return True
        except Exception:
            return False
