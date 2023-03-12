"""pyShelf's main frontend library."""
import uvicorn
import os
import sass
import datetime
# import gzip
# import brotli
from json import dumps
from base64 import b64encode
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ...backend.lib.storage import Storage
from .objects import JSInterface
from ...backend.lib.config import Config

app = FastAPI()
templates = Jinja2Templates(directory="src/frontend/templates")


def base64decode(string) -> str:
    """Decode a base64 string."""
    try:
        result = b64encode(string).decode("utf-8")
    except Exception:
        result = "None"
    return result


def summarize(string) -> str:
    """Summarize a string."""
    try:
        if len(string) > 50:
            return string[:50] + "..."
        return string
    except TypeError:
        return "None"


def convertDateTime(timestamp: datetime) -> str:
    """Convert a datetime object to a string."""
    return timestamp.strftime("%d/%m/%Y %H:%M:%S")


def books_tojson(obj) -> dumps:
    """Convert an object to a dictionary."""
    _books: list = []
    for book in obj:
        _books.append({
            "book_id": book[0].book_id,
            "title": book[0].title,
            "author": book[0].author,
            "categories": book[0].categories,
            "cover": base64decode(book[0].cover),
            "pages": book[0].pages,
            "progress": book[0].progress,
            "file_name": book[0].file_name,
            "description": book[0].description,
            "date": convertDateTime(book[0].date),
            "rights": book[0].rights,
            "tags": book[0].tags,
            "identifier": book[0].identifier,
            "publisher": book[0].publisher,
        })
    # compressed = gzip.compress(dumps(_books).encode("utf-8"))
    # compressed = gzip.compress(dumps(_books).encode())
    return dumps(_books)


def book_tojson(book) -> dumps:
    """Convert a book object to a json."""
    return dumps({
            "book_id": book[0].book_id,
            "title": book[0].title,
            "author": book[0].author,
            "categories": book[0].categories,
            "cover": base64decode(book[0].cover),
            "pages": book[0].pages,
            "progress": book[0].progress,
            "file_name": book[0].file_name,
            "description": book[0].description,
            "date": convertDateTime(book[0].date),
            "rights": book[0].rights,
            "tags": book[0].tags,
            "identifier": book[0].identifier,
            "publisher": book[0].publisher,
        })


def collections_tojson(collection) -> dumps:
    """Convert a collections object to json."""
    _collections = []
    for _collection in collection:
        _collections.append({
            "collection_id": _collection[0].collection_id,
            "book_id": _collection[0].book_id,
            "collection": _collection[0].collection,
        })
    return dumps(_collections)


templates.env.filters["b64decode"] = base64decode
templates.env.filters["summarize"] = summarize
templates.env.filters["books_tojson"] = books_tojson


class FastAPIServer():
    """Entry point for FastAPI server."""

    def __init__(self, config):
        """Initialize FastAPIServer object parameters."""
        self.config = config
        app.mount("/static",
                  StaticFiles(directory="src/frontend/static"),
                  name="static")
        self.fe_config = uvicorn.Config(app, port=8080,
                                        log_level="info", reload=True)
        self.fe_server = uvicorn.Server(self.fe_config)
        self.JSInterface: JSInterface = JSInterface(self.config)
        self.compile_static_files()

    def compile_static_files(self):
        """Compile static files for web frontend."""
        _pyShelf_src = sass.compile(
            filename='src/frontend/static/styles/pyShelf.sass',
            source_map_filename='src/frontend/static/styles/pyShelf.sass',
            output_style='compressed')
        with open('src/frontend/static/styles/pyShelf.css', 'w') as _pyShelf:
            _pyShelf.write(_pyShelf_src[0])
        _pyShelf.close()
        self.JSInterface.install()
        return True

    def use_route_names_as_operation_ids(self, app: FastAPI) -> None:
        """Use route name as operation id."""
        for route in app.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request, skip: int = 0, limit: int = 10):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        books = storage.get_books(collection=None, skip=skip, limit=limit)
        """Home page responder."""
        context = {"request": request, "books": books}
        return templates.TemplateResponse("index.html", context)

    @app.get("/books", response_class=JSONResponse)
    async def books(request: Request, skip: int = 0, limit: int = 10, collection=None):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        books = storage.get_books(collection, skip=skip, limit=limit)
        headers = {"Accept-Encoding": "gzip"}
        """Home page responder."""
        return JSONResponse(content=books_tojson(books))

    @app.get("/book/{book_id}", response_class=JSONResponse)
    async def book(request: Request, book_id: int):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        book = storage.get_book(book_id)
        """Home page responder."""
        return JSONResponse(content=book_tojson(book))

    @app.get("/collections", response_class=JSONResponse)
    async def collections(request: Request):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        collections = storage.get_collections()
        """Home page responder."""
        return JSONResponse(content=collections_tojson(collections))


    async def run(self):
        """Front end server entrypoint."""
        self.config.logger.info("Starting FastAPI server.")
        self.use_route_names_as_operation_ids(app)
        await self.fe_server.serve()
