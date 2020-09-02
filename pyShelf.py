#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

import websockets

from src.backend.lib.config import Config
from src.backend.pyShelf_MakeCollections import MakeCollections
from src.backend.pyShelf_ScanLibrary import execute_scan

root = Path.cwd()
config = Config(root)
PRG_PATH = Path.cwd().__str__()
sys.path.insert(0, PRG_PATH)

tx = None


async def runImport():
    execute_scan(PRG_PATH, config=config)
    MakeCollections(PRG_PATH, config=config)
    return "Import Complete"


async def socketio(websocket, path):
    async for message in websocket:
        config.logger.info("Message Processing")
        if message == "ping":
            config.logger.info("<< Ping")
            tx = pong(message)
        elif message == "importBooks":
            config.logger.info("Starting Import")
            tx = "Starting Import . . ."
            await websocket.send(tx)
            await runImport()
            tx = "complete"
        await websocket.send(tx)


def pong(message):
    config.logger.info(">> Pong")
    return "pong"


start_server = websockets.serve(socketio, "127.0.0.1", 1337)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
