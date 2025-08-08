#!/bin/sh
set -e  # Exit on error

cd /tmp/
git clone https://github.com/th3r00t/pyShelf.git
cd /tmp/pyShelf/

# Ensure the correct branch is checked out before installing dependencies
git fetch origin
git checkout 0.8.0--dev-zipapp

# Install dependencies in the correct branch context
uv sync
#export project dependencies to requirements.txt
uv export --requirements > requirements.txt
# Install Python dependencies
pipx install -r requirements.txt

# Build the release
./build.sh

# Install assets
sudo mkdir -p /var/lib/pyshelf/assets
sudo cp -r ./src/frontend/static /var/lib/pyshelf/assets
sudo cp -r ./src/frontend/templates /var/lib/pyshelf/assets

# Install executable
sudo cp ./release/pyshelf /usr/local/bin/pyshelf

