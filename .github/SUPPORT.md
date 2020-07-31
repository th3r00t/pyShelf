## Getting Help With **pyShelf**

If you have issues during initial setup please make sure you have a working Web Server (the pyShelf team recommends [NGINX](https://nginx.com), and that you have correctly setup your webserver to forward cgi requests to [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/Download.html). Additionaly uWSGI must be setup to serve the application. A sample NGINX config (**pyshelf_nginx.conf**), and (**uwsgi.ini**) are included in the project root.
**<p align=center>Ensure your Webserver has appropriate access to your install directory!</p>**

### pyshelf_nginx.conf
```
# the upstream component nginx needs to connect to
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}
```
* Set `server 127.0.0.1:8001`, this must match the socket decleration in your uwsgi config **uwsgi.ini**.
```
# configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name 127.0.0.1; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste
```
* Set `listen   8000;`  to the port you want to serve the frontend on
* Set `server_name 127.0.0.1;` to the ip address, or FQDN of your server
```
    # Django media
    location /media  {
        alias /home/raelon/Projects/pyShelf/frontend/interface/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /home/raelon/Projects/pyShelf/frontend/interface/static; # your Django project's static files - amend as required
    }

    location /books {
        internal;
        alias   /home/raelon/Projects/pyShelf/books;
        # Absolute location of your ebook files
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /home/raelon/Projects/pyShelf/uwsgi_params; # the uwsgi_params file you installed
    }
}
```
* Adjust all the `alias /home/raelon/Project/pyShelf` entries to match your install directory ensure you **do not change** the `/frontend/interface/media` or `/frontend/interface/static` portions
* Adjust `alias /home/raelon/Projects/pyShelf/books` to match the location of your books

### uwsgi.ini
```
[uwsgi]
# chdir = {Full path to pyShelf/frontend}
chdir=/home/raelon/Projects/pyShelf/src
module=frontend.wsgi
master=True
pidfile=/tmp/pyShelf.pid
vacuum=True
socket=127.0.0.1:8001
```
* Set `chdir=/home/raelon/Projects/pyshelf` leaving `/src` **intact** to match your install directory
* Set `socket=127.0.0.1:8001` to match the entry as defined above in `upstream django{`

Now you may restart your webserver to apply the changes, and then either run `uwsgi -i uwsgi.ini` fron the project root, or restart your uwsgi service.

### Import your books
* Run `./importBooks` in your project root

### Access pyShelf's frontend
* Browse to `http://localhost:8000` _substitute ip:port as defined in your webserver_ and you should be greeted by the pyShelf frontend.

### Still Stuck?
Please contact us using any of the options below for support. Please be prepared with your nginx error logs.

### Via Email
* Support Email: [support@pyshelf.com](mailto://support@pyshelf.com)

### Live Support Options
* Discord: [https://discord.gg/H9TbNJS](https://discord.gg/H9TbNJS)
* IRC: [irc.freenode.net/pyShelf](irc://freenode.net/pyshelf)
* Matrix.org: [#irc_#pyshelf:pyshelf.com](https://app.element.io/#/room/#irc_#pyshelf:pyshelf.com)
