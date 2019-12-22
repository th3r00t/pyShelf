#!/usr/bin/python

import pathlib
import sys

PRG_PATH = pathlib.Path.cwd()
LIB_PATH = pathlib.Path.joinpath(PRG_PATH, "src", "backend", "lib")
sys.path.insert(0, PRG_PATH)
