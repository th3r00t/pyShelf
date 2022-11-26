"""pyShelf's main frontend library."""
import uvicorn
import sass
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="src/frontend/templates")


class FastAPIServer():

    def __init__(self, config):
        self.config = config
        app.mount("/static",
                  StaticFiles(directory="src/frontend/static"),
                  name="static")
        self.fe_config = uvicorn.Config(app, port=8080,
                                        log_level="info", reload=True)
        self.fe_server = uvicorn.Server(self.fe_config)
        self.compile_static_files()

    def compile_static_files(self):
        """Compile static files for web frontend."""
        _pyShelf_src = sass.compile(
            filename='src/frontend/static/styles/pyShelf.sass',
            source_map_filename='src/frontend/node_modules/bulma/bulma.sass',
            output_style='compressed'
        )
        with open('src/frontend/static/styles/pyShelf.css', 'w') as _pyShelf:
            _pyShelf.write(_pyShelf_src[0])
        _pyShelf.close()
        return True

    def use_route_names_as_operation_ids(self, app: FastAPI) -> None:
        """Use route name as operation id."""
        for route in app.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Home page responder."""
        return templates.TemplateResponse(
            "index.html",
            {"request": request})

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
