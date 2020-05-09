#!/usr/bin/env bash
eval python3 preinstall
eval "pip install -r requirements.txt"
eval python3 installer
