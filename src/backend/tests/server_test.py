#!/usr/bin/env python3
from src.backend.lib.pyShelf import Server

def test_start():
    server = await Server().start()
    assert Server().start() is True
