#!/usr/bin/env python3
import asyncio
import websockets
import sys
from pathlib import Path
from loguru import logger
from src.backend.lib.config import Config
from src.backend.pyShelf_ScanLibrary import execute_scan
from src.backend.pyShelf_MakeCollections import MakeCollections


root = Path.cwd()
config = Config(root)
PRG_PATH = Path.cwd().__str__()
sys.path.insert(0, PRG_PATH)

tx = None


async def runImport():
    execute_scan(PRG_PATH)
    MakeCollections(PRG_PATH)
    return "Import Complete"


async def socketio(websocket, path):
    async for message in websocket:
        if message == "import":
            print("message from Con1 >> {}".format(message))
            tx = "ack->{}".format(message)
        elif message == "Connection 2":
            print("message from Con2 >> {}".format(message))
            tx = "ack->{}".format(message)
        elif message == "ping":
            print("<<[{}]".format(message))
            tx = pong(message)
        elif message == "importBooks":
            print("<<[{} cmd rcvd]\n Starting import".format(message))
            tx = "Starting Import . . ."
            await websocket.send(tx)
            await runImport()
            tx = "complete"

        await websocket.send(tx)


def pong(message):
    print('Ping Received')
    return "pong"


start_server = websockets.serve(socketio, "127.0.0.1", 1337)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
