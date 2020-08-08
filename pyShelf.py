#!/usr/bin/env python3
import asyncio
import websockets
from pathlib import Path
from src.backend.lib.config import Config

root = Path.cwd()
config = Config(root)


async def echo(websocket, path):
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
        await websocket.send(tx)

def pong(message):
    return "pong"

start_server = websockets.serve(echo, "127.0.0.1", 1337)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
