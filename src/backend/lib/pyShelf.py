#!/usr/bin/env python3
import asyncio
import os
import time

import websockets

from .config import Config
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

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.instance = None

    async def entrypoint(self, websocket, path):
        _str = await websocket.recv()
        greeting = f"{_str}"
        await websocket.send(greeting)

    async def start(self):
        try:
            self.instance = await websockets.serve(self.entrypoint, "localhost", 1337)
            return True
        except Exception:
            raise
