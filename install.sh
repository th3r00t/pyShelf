#!/bin/env bash

cd /tmp/
git clone https://github.com/th3r00t/pyShelf.git
cd /tmp/pyShelf/

# create pyshelf system user if it doesn't exist
if ! id -u pyshelf >/dev/null 2>&1; then
	sudo useradd -r -s /usr/bin/nologin pyshelfA
	sudo mkdir -p /home/pyshelf
	sudo chown pyshelf:pyshelf /home/pyshelf
	sudo chmod 755 /home/pyshelf
fi
# make home dir for pyshelf user if it doesn't exist
if [ ! -d /home/pyshelf ]; then
	sudo mkdir -p /home/pyshelf
	sudo chown pyshelf:pyshelf /home/pyshelf
	sudo chmod 755 /home/pyshelf
fi

# Ensure the correct branch is checked out before installing dependencies
git fetch origin
git checkout 0.8.0--dev-zipapp

# if on arch linux, install python3-uv
if [ -f /etc/arch-release ]; then
	sudo pacman --noconfirm -Syy python-uv
else
	sudo apt-get update
	sudo apt-get install -y python3-uv python3 python3-pip nodejs npm libxml2 libxslt1-dev zlib1g-dev libjpeg-turbo8-dev build-essential
fi

sudo mkdir /etc/pyShelf
sudo cp -avR . /etc/pyShelf
cd /etc/pyShelf
sudo uv sync
# sudo mkdir release
cd /etc/pyShelf/src/frontend
echo "Installing frontend dependencies..."
sudo npm install
cd /etc/pyShelf
echo "Building frontend..."
if [ ! -d /etc/pyShelf/release ]; then
	sudo mkdir release
fi
echo "Building release..."
sudo ./build.sh
echo "Linking executable..."
sudo ln -s /etc/pyShelf/pyshelf.sh /usr/local/bin/
echo "Installing systemd service..."
if [ -f /usr/lib/systemd/system/pyShelf.service ]; then
	sudo rm /usr/lib/systemd/system/pyShelf.service
fi
sudo cp /tmp/pyShelf/pyShelf.service /usr/lib/systemd/system/
echo "Enabling systemd service..."
sudo systemctl daemon-reload
sudo systemctl enable --now pyShelf.service
echo "Installation complete."
echo "You can now access pyShelf at http://localhost:8000"
echo "If your books are not at /mnt/books, please edit the config file at \
	/etc/pyShelf/config.json"

