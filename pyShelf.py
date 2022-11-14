#!/usr/bin/env python3
"""PyShelf Entrypoint."""
import asyncio
import sys
from pathlib import Path
from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute

from src.backend.lib.config import Config
from src.backend.pyShelf_MakeCollections import MakeCollections
from src.backend.pyShelf_ScanLibrary import execute_scan

# import websockets


root = Path.cwd()
config = Config(root)
PRG_PATH = Path.cwd().__str__()
sys.path.insert(0, PRG_PATH)
app = FastAPI()


def RunImport():
    """Begin live import of books."""
    config.logger.info("Begining book import.")
    execute_scan(PRG_PATH, config=config)
    config.logger.info("Finished book import.")
    MakeCollections(PRG_PATH, config=config)
    return "Import Complete"


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>pyShelf eBook Server</title>
        </head>
        <body>
            <h3>pyShelf Open Source Content Server</h3>
        </body>
    </html>
    """


@app.get("/users/me")
async def about_me():
    return {"user_id": "CurrentUser"}


@app.get("/users/{user_id}")
async def about_user(user_id: int):
    return {"user_id": user_id}


@app.get("/dev/test/echo/{_test_item_}")
async def echo_test(_test_item_):
    return {"Test Object": _test_item_}


async def fe_server():
    config.logger.info("Starting FastAPI server.")
    fe_config = uvicorn.Config("__main__:app", port=8080, log_level="info", reload=True)
    fe_server = uvicorn.Server(fe_config)
    await fe_server.serve()


async def main():
    _import_thread = Thread(target=RunImport)
    _import_thread.start()
    asyncio.create_task(fe_server())


if __name__ == "__main__":
    use_route_names_as_operation_ids(app)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
    loop.close()
    exit
    # asyncio.get_event_loop(asyncio.run(main())).run_forever()
