#!/bin/sh
set -e  # Exit on error

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
	sudo pacman -Syy python-uv
	sudo mkdir /etc/pyShelf
	sudo cp -avR . /etc/pyShelf
	cd /etc/pyShelf
	# sudo chown -R pyshelf:pyshelf /etc/pyShelf
	# sudo chmod -R 755 /etc/pyShelf
	# sudo -u pyshelf uv sync
	# sudo -u pyshelf mkdir release
	sudo uv sync
	cd /etc/pyShelf/src/frontend
	sudo npm install
	sudo mkdir release
	# sudo -u pyshelf direnv allow
else
	sudo apt-get update
	sudo apt-get install -y python3-uv python3 python3-pip nodejs npm libxml2 libxslt1-dev zlib1g-dev libjpeg-turbo8-dev build-essential
	sudo pip install -r requirements.txt
fi

# Build the release
cd /etc/pyShelf
sudo ./build.sh

# Install assets
# sudo mkdir -p /var/lib/pyshelf/assets
# sudo cp -r ./src/frontend/static /var/lib/pyshelf/assets
# sudo cp -r ./src/frontend/templates /var/lib/pyshelf/assets

# Install executable
# sudo cp ./release/pyshelf /usr/local/bin/pyshelf
sudo ln -s /etc/pyShelf/pyshelf.sh /usr/local/bin/
# Make sure the executable is owned by the pyshelf user
# sudo chown pyshelf:pyshelf /usr/local/bin/pyshelf.sh
# Make the executable accessible
# sudo chmod 755 /usr/local/bin/pyshelf.sh
# sudo chown pyshelf:pyshelf /usr/local/bin/pyshelf

