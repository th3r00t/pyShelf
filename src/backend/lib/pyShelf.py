#!/usr/bin/env python3
import asyncio
import os
import sys
import time

import websockets

from .config import Config
from .library import Catalogue
from .storage import Storage


class InitFiles:
    """First run file creation operations"""
    def __init__(self, file_array):
        for _pointer in file_array:
            time.sleep(1)
            if not os.path.isfile(_pointer):
                self.CreateFile(_pointer)
        time.sleep(1)

    def CreateFile(self, _pointer):
        """
        Checks if file exists and creates it if not
        """
        if not os.path.isdir(os.path.split(_pointer)[0]):
            os.mkdir(os.path.split(_pointer)[0])
            f = open(_pointer, "w+")
            f.close()


class Server:
    """
    Main Server Container
    :TODO: Document this
    """

    async def __init__(self, root):
        self.root = root
        self.config = Config(self.root)
        self.instance = None
        self.serve = await websockets.serve(socketio, "127.0.0.1", 1337)

    async def __aexit__(self, *args, **kwargs):
        await self.serve.__aexit__(*args, **kwargs)

    async def runImport(self):
        _start_time = time.time()
        InitFiles(self.config.file_array)
        _storage = Storage(self.config)
        _storage.check_ownership()
        Catalogue(self.config).import_books()
        _storage.make_collections()
        _total_time = round(time.time() - _start_time)

    async def socketio(self, websocket, path):
        async for message in websocket:
            if message == "ping":
                config.logger.info("<< Ping")
                tx = self.pong()
            elif message == "importBooks":
                config.logger.info("Starting Import")
                tx = "Starting Import . . ."
                await websocket.send(tx)
                await runImport()
                tx = "complete"
            await websocket.send(tx)

    def pong(self):
        self.config.logger.info(">> Pong")
        return "pong"

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.serve)
