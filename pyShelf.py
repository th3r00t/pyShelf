#!/usr/bin/env python3
"""PyShelf Entrypoint."""
import asyncio
import sys
from pathlib import Path
from threading import Thread

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.backend.lib.config import Config
from src.backend.pyShelf_MakeCollections import MakeCollections
from src.backend.pyShelf_ScanLibrary import execute_scan
# import websockets


root = Path.cwd()
config = Config(root)
PRG_PATH = Path.cwd().__str__()
sys.path.insert(0, PRG_PATH)
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
templates = Jinja2Templates(directory="src/frontend/templates")

def RunImport():
    """Begin live import of books."""
    config.logger.info("Begining book import.")
    execute_scan(PRG_PATH, config=config)
    config.logger.info("Finished book import.")
    MakeCollections(PRG_PATH, config=config)
    return "Import Complete"


def use_route_names_as_operation_ids(app: FastAPI) -> None:
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


async def fe_server():
    """Front end server entrypoint."""
    config.logger.info("Starting FastAPI server.")
    fe_config = uvicorn.Config("__main__:app", port=8080,
                               log_level="info", reload=True)
    fe_server = uvicorn.Server(fe_config)
    await fe_server.serve()


async def main():
    """Program entrypoint."""
    _import_thread = Thread(target=RunImport)
    _import_thread.start()
    _task = await asyncio.create_task(fe_server())
    return [_task, _import_thread]


if __name__ == "__main__":
    use_route_names_as_operation_ids(app)
    asyncio.run(main())
    sys.exit(0)
