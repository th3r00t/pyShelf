"""pyShelf's main frontend library."""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="src/frontend/templates")
class FrontendServer():

    def __init__(self, config):
        self.config = config
        app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")


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
    async def about_me():
        """About me page responder."""
        return {"user_id": "CurrentUser"}


    @app.get("/users/{user_id}")
    async def about_user(user_id: int):
        """About user page responder."""
        return {"user_id": user_id}


    @app.get("/dev/test/echo/{_test_item_}")
    async def echo_test(_test_item_):
        """Test echo responder function."""
        return {"Test Object": _test_item_}


    async def run(self):
        """Front end server entrypoint."""
        self.config.logger.info("Starting FastAPI server.")
        self.use_route_names_as_operation_ids(app)
        self.fe_config = uvicorn.Config(app, port=8080,
                                log_level="info", reload=True)
        self.fe_server = uvicorn.Server(self.fe_config)
        await self.fe_server.serve()
