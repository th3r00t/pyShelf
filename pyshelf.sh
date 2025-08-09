#!/usr/bin/sh
# This script is used to run the pyshelf application.
# It sets up the environment and runs the main script.
# first we need to activate the virtual environment
if [ -d "/etc/pyShelf/.venv" ]; then
	source /etc/pyShelf/.venv/bin/activate
else
	echo "Virtual environment not found. Please create it first."
	exit 1
fi
# then we need to run the main script
if [ -f "/etc/pyShelf/release/pyshelf" ]; then
	exec /etc/pyShelf/release/pyshelf	
else
	echo "Main script not found. Please check the directory."
	exit 1
fi
