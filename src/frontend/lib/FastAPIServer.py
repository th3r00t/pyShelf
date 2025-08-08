"""pyShelf's main frontend library."""
import uvicorn
import os
import sass
import datetime
import math
# import gzip
# import brotli
from json import dumps
from base64 import b64encode
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.lib.storage import Storage
from .objects import JSInterface
from .runtime_paths import ensure_assets
from backend.lib.config import Config

app = FastAPI()
STATIC_DIR, TEMPLATES_DIR = ensure_assets()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
# templates = Jinja2Templates(directory="src/frontend/templates")
origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:8080",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        convert_none = lambda x: x if x is not None else "None"
        _books.append({
            "book_id": book.id,
            "title": book.title,
            "author": book.author,
            "categories": convert_none(book.categories),
            "cover": base64decode(book.cover),
            "pages": convert_none(book.pages),
            "progress": convert_none(book.progress),
            "file_name": book.file_name,
            "description": convert_none(book.description),
            "date": convertDateTime(book.date),
            "rights": convert_none(book.rights),
            "tags": convert_none(book.tags),
            "identifier": convert_none(book.identifier),
            "publisher": convert_none(book.publisher),
        })
    return dumps(_books)


def book_tojson(book) -> dumps:
    """Convert a book object to a json."""
    return dumps({
        "book_id": book.id,
        "title": book.title,
        "author": book.author,
        "categories": book.categories,
        "cover": base64decode(book.cover),
        "pages": book.pages,
        "progress": book.progress,
        "file_name": book.file_name,
        "description": book.description,
        "date": convertDateTime(book.date),
        "rights": book.rights,
        "tags": book.tags,
        "identifier": book.identifier,
        "publisher": book.publisher,
    })

def tojson(obj) -> dumps:
    return dumps(obj)

def collections_tojson(collection) -> dumps:
    """Convert a collections object to json."""
    _collections = []
    _collection_id_set = set()
    for _collection in collection:
        if _collection.id in _collection_id_set:
            pass
        else:
            _collection_id_set.add(_collection.id)
            _collections.append({
                "collection_id": _collection.id,
                "collection": _collection.name,
            })
    return dumps(_collections)


templates.env.filters["b64decode"] = base64decode
templates.env.filters["summarize"] = summarize
templates.env.filters["books_tojson"] = books_tojson
templates.env.filters["collections_tojson"] = collections_tojson
templates.env.filters["tojson"] = tojson


class FastAPIServer():
    """Entry point for FastAPI server."""

    def __init__(self, config):
        """Initialize FastAPIServer object parameters."""
        self.config = config
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
        # app.mount("/static",
        #           StaticFiles(directory="src/frontend/static"),
        #           name="static")
        self.fe_config = uvicorn.Config(app, host="0.0.0.0", port=8080,
                                        log_level="info", reload=True)
        self.fe_server = uvicorn.Server(self.fe_config)
        self.JSInterface: JSInterface = JSInterface(self.config)
        self.compile_static_files()

    def compile_static_files(self):
        """Compile static files for web frontend."""
        _pyShelf_src = sass.compile(
            filename='src/frontend/static/styles/pyShelf.sass',
            source_map_filename='src/frontend/static/styles/pyShelf.sass',
            output_style='compressed',
            include_paths=[
                'node_modules',
                'src/frontend/static/styles'
            ]
        )
        with open('src/frontend/static/styles/pyShelf.css', 'w') as _pyShelf:
            _pyShelf.write(_pyShelf_src[0])

        self.JSInterface.install()
        return True

    def use_route_names_as_operation_ids(self, app: FastAPI) -> None:
        """Use route name as operation id."""
        for route in app.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request, skip: int = 0, limit: int = 30):
        if skip <= 0:
            skip_num = 0
            skip = 0
        else:
            skip_num = skip * limit
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        books = storage.get_books(collection=None, skip=skip_num, limit=limit)
        collections = storage.get_collections()
        """Home page responder."""
        total_books = len(storage.get_books())
        if skip <= 0:
            skip_num = 0
            skip = 0
        else:
            skip_num = skip * limit
        context = {
            "request": request,
            "total_pages": math.ceil(total_books / limit),
            "books": books,
            "collections": collections,
            "page": skip,
            "limit": limit
        }
        return templates.TemplateResponse("index.html", context)

    @app.get("/api/books", response_class=JSONResponse)
    async def books(request: Request, skip: int = 0, limit: int = 10, collection=None):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        books = storage.get_books(collection, skip=skip, limit=limit)
        headers = {"Accept-Encoding": "gzip"}
        """Home page responder."""
        return JSONResponse(content=books_tojson(books))
        # return JSONResponse(content=books)

    @app.get("/api/book/{book_id}", response_class=JSONResponse)
    async def book(request: Request, book_id: int):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        book = storage.get_book(book_id)
        """Home page responder."""
        return JSONResponse(content=book_tojson(book))

    @app.get("/api/get_book/{book_id}", response_class=FileResponse)
    async def book(request: Request, book_id: int):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        book = storage.get_book(book_id)
        file_path = book[0].file_name
        if not os.path.exists(file_path):
            return JSONResponse(status_code=404, content={"error": "File not found"})
        """Book file responder."""
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type="application/octet-stream")

    @app.get("/api/collections", response_class=JSONResponse)
    async def collections(request: Request):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        collections = storage.get_collections()
        """Home page responder."""
        return JSONResponse(content=collections_tojson(collections))

    @app.get("/api/collection/{collection}", response_class=HTMLResponse)
    async def collection(request: Request, collection: str, skip:int=0, limit:int=30):
        """Collection file responder."""
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        if skip <= 0:
            skip_num = 0
            skip = 0
        else:
            skip_num = skip * limit
        books = storage.get_books(collection, skip=skip_num, limit=limit)
        total_books = len(storage.get_books(collection))
        collections = storage.get_collections()
        context = {
            "request": request,
            "books": books,
            "collections": collections,
            "collection": collection,
            "total_pages": math.ceil(total_books / limit),
            "page": skip,
            "limit": limit
        }
        return templates.TemplateResponse("collection.html", context)
    
    @app.get("/api/search", response_class=HTMLResponse)
    async def search_books_api(request: Request, search: str):
        """Collection file responder."""
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        books = storage.fuzzy_search_books(search)
        total_books = len(books)
        collections = storage.get_collections()
        context = {
            "request": request,
            "books": books,
            "collections": collections,
            "total_pages": 1,
            "total_books": total_books,
        }
        return templates.TemplateResponse("search.html", context)

    async def run(self):
        """Front end server entrypoint."""
        self.config.logger.info("Starting FastAPI server.")
        self.use_route_names_as_operation_ids(app)
        await self.fe_server.serve()
