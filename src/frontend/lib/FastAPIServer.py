"""pyShelf's main frontend library."""
import uvicorn
import os
import sass
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ...backend.lib.storage import Storage
from .objects import JSInterface
from ...backend.lib.config import Config

app = FastAPI()
templates = Jinja2Templates(directory="src/frontend/templates")


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
    async def index(request: Request):
        storage = Storage(Config(os.path.abspath(os.getcwd())))
        books = storage.get_books()
        """Home page responder."""
        # _books = self.storage.get_books()
        context = {"request": request, "books": books}
        return templates.TemplateResponse("index.html", context )

    @app.get("/users/me")
    async def about_me(self):
        """About me page responder."""
        return {"user_id": "CurrentUser"}

    @app.get("/users/{user_id}")
    async def about_user(self, user_id: int):
        """About user page responder."""
        return {"user_id": user_id}

    @app.get("/dev/test/echo/{_test_item_}")
    async def echo_test(self, _test_item_):
        """Test echo responder function."""
        return {"Test Object": _test_item_}

    async def run(self):
        """Front end server entrypoint."""
        self.config.logger.info("Starting FastAPI server.")
        self.use_route_names_as_operation_ids(app)
        await self.fe_server.serve()
