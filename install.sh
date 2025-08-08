#!/bin/sh
set -e  # Exit on error

cd /tmp/
git clone https://github.com/th3r00t/pyShelf.git
cd /tmp/pyShelf/

# Ensure the correct branch is checked out before installing dependencies
git fetch origin
git checkout 0.8.0--dev-zipapp

# if on arch linux, install python3-uv
if [ -f /etc/arch-release ]; then
	sudo pacman -S --needed python-uv python python-pip python-pipx nodejs npm\
		libxml2 libxslt zlib libjpeg-turbo gcc base-devel python-loguru\
		python-rapidfuzz
	pipx install . --include-deps
	pipx ensurepath
else
	sudo apt-get update
	sudo apt-get install -y python3-uv python3 python3-pip nodejs npm libxml2 libxslt1-dev zlib1g-dev libjpeg-turbo8-dev build-essential
	sudo pip install -r requirements.txt
fi

# Build the release
./build.sh

# Install assets
sudo mkdir -p /var/lib/pyshelf/assets
sudo cp -r ./src/frontend/static /var/lib/pyshelf/assets
sudo cp -r ./src/frontend/templates /var/lib/pyshelf/assets

# Install executable
sudo cp ./release/pyshelf /usr/local/bin/pyshelf

