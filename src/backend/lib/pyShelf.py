#!/usr/bin/env python3
import asyncio
import os
import time
import datetime
import websockets

from .config import Config
from .library import Catalogue
from .storage import Storage
from django.conf import settings
import psycopg2
from django.contrib.auth.hashers import make_password

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]


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

    def __init__(self, root):
        self.root = root
        self.host = ("127.0.0.1", 1337)
        self.config = Config(self.root)
        self.loop = None
        self.serve = None

    async def __aexit__(self, *args, **kwargs):
        await self.serve.__aexit__(*args, **kwargs)

    async def initialize_server(self):
        self.config.logger.info("INITIALIZE")
        self.serve = await websockets.serve(self.socketio, self.host[0], self.host[1])
        await asyncio.sleep(.01)
        self.config.logger.info("Server Initialization Complete")

    async def runImport(self):
        _start_time = time.time()
        InitFiles(self.config.file_array)
        _storage = Storage(self.config)
        _storage.check_ownership()
        Catalogue(self.config).import_books()
        _storage.make_collections()
        _total_time = round(time.time() - _start_time)

    async def socketio(self, websocket, path):
        self.config.logger.info("Listener Starting")
        async for message in websocket:
            if message == "ping":
                self.config.logger.info("<< Ping")
                tx = self.pong()
            elif message == "importBooks":
                self.config.logger.info("Starting Import")
                tx = "Starting Import . . ."
                await websocket.send(tx)
                await asyncio.sleep(0.01)
                await self.runImport()
                await asyncio.sleep(0.01)
                tx = "complete"
            else:
                self.config.logger.info("Unhandled Message Rcvd :: {}".format(message))
            await websocket.send(tx)

    def pong(self):
        self.config.logger.info(">> Pong")
        return "pong"

    async def start(self):
        self.loop = asyncio.get_running_loop()
        self.loop.set_debug(True)
        await websockets.serve(self.socketio, self.host[0], self.host[1])
        await asyncio.sleep(1)


class Admin:

    def __init__(self, root):
        self.config = Config(root)
        self.db = Storage(self.config)
        settings.configure()

    def createsuperuser(self):
        self.db.cursor.execute("SELECT * FROM interface_user")
        _user_list = self.db.cursor.fetchall()
        if len(_user_list) > 0:
            return False
        else:
            today = datetime.date.today()
            date = psycopg2.Date(today.year, today.month, today.day)
            self.db.cursor.execute(
                'INSERT INTO interface_user (username, password, is_staff, is_active, is_superuser, '
                'date_joined, first_name, last_name, ulvl, email ) '
                'VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                ("pyshelf", make_password("pyshelf"), True, True, True, date, "pyshelf", "default", 1,
                 "change_or@delete.me"))
            self.db.commit()
            self.db.close()
            return True
