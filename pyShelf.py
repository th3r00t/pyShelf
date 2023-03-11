#!/usr/bin/env python3
"""PyShelf Entrypoint."""
import asyncio
import sys
from pathlib import Path
from threading import Thread
from src.backend.lib.config import Config
from src.backend.pyShelf_MakeCollections import MakeCollections
from src.backend.pyShelf_ScanLibrary import execute_scan
from src.frontend.lib.FastAPIServer import FastAPIServer
from src.frontend.lib.objects import FastAPIServer
# import websockets


root = Path.cwd()
config = Config(root)
PRG_PATH = Path.cwd().__str__()
sys.path.insert(0, PRG_PATH)


def run_import():
    """Begin live import of books."""
    config.logger.info("Begining book import.")
    execute_scan(PRG_PATH, config=config)
    config.logger.info("Finished book import.")
    MakeCollections(PRG_PATH, config=config)
    return "Import Complete"


async def main():
    """Program entrypoint."""
    _import_thread = Thread(target=run_import)
    _import_thread.start()
    fe_server = FastAPIServer(config)
    _task = await asyncio.create_task(fe_server.run())
    return [_task, _import_thread]


if __name__ == "__main__":
    asyncio.run(main())
    sys.exit(0)
