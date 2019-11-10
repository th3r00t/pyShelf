#!/usr/bin/python
import cgi
import sys

from config import Config

sys.path.insert(0, '../')


class Frontend():
    """Dynamic frontend display functions"""

    def __init__(self, dimensions=[0, 0]):
        """
        :param dimensions: array containing screen size [x, y]
        """
        self.dimensions = dimensions
        self.TITLE = Config().TITLE

    def html_Headers(self):
        """
        HTML headers
        :returns _head: HTML render of page headers
        """
        _head = """
        <!DOCTYPE html>
        <html lang=\"en\">
        <head>
        <meta charset=\"utf-8\">
        <meta http-equiv=\"X-UA-Compatible\" content=\"IE-edge\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <link type=\"text/css\" rel=\"stylesheet\" href=\"/css/main.css\" />
        <title>%s</title>
        </head>
        """ % self.TITLE
        return _head

    def app_Headers(self):
        """
        App specific headers
        :returns _head: HTML render of application specific headers
        """
        _head = """
        <body>
        <div id=\"app\">
        <div class=\"app_header\">
        <h1 class=\"app_hdr shadow\">pyShelf</h1>
        <h2> class=\"app_subhdr shadow\">Open Source E-book Server</h2>
        </div>
        """
        return _head

    def app_body(self, nav, shelf):
        """
        Main interface body, and navigation
        :param nav: nav[] system navigation list
        :param shelf: shelf[0{path:"",title:"",cover:"",author:""}]
        :returns _body: HTML render of page body
        """
        _body = """
        <div class=\"app_body\">
        <div class=\"left_col\">
        %s
        </div>
        <div class=\"shelf\">
        <div class=\"shelf_contents\">
        %s
        </div>
        </div>
        </div>
        """ %(nav, shelf)
        return _body

    def app_footer(self):
        """
        Main interface footer; Closes HTML
        :returns _footer: HTML render of page footer
        """
        _footer = """
        <div class=\"app_footer\">
        <div class=\"python_logo\">
        <img src=\"/img/py.png\" id=\"python_logo\" />
        </div>
        </div>
        </div>
        </body>
        </html>
        """
        return _footer

    def compile(self, nav, shelf):
        """
        Compiles user interface
        :returns _ui: Compiled HTML for page layout
        """
        _head = self.html_Headers() + self.app_Headers()
        _body = self.app_body(nav, shelf)
        _foot = self.app_footer()
        try:
            _ui = _head + _body + _foot
            return _ui
        except Exception as e:
            return e
