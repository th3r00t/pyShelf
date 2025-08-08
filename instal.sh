cd /tmp/
git clone https://github.com/th3r00t/pyShelf.git
cd pyshelf
git checkout 0.8.0--dev-zipapp
./build.sh
sudo cp ./src/frontend/static /var/lib/pyshelf/assets -r
sudo cp ./src/frontend/templates /var/lib/pyshelf/assets -r
sudo cp ./release/pyshelf /usr/local/bin/pyshelf
