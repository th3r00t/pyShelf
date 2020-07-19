import os
from base64 import b64decode, b64encode
from pathlib import Path

from backend.lib.config import Config
from django.db import models
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect # render_to_response
from django.utils.text import slugify
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import json
from .forms import SignUpForm, UserLoginForm
from .models import Books, Collections, Navigation, Favorites

config = Config(Path("../"))

collections = Collections.objects.all()


def index(request, query=None, _set=1, _limit=None, _order='title'):
    """
    Return template index
    """
    _payload = payload(request, query, _set, _limit, _order)
    return render(
        request,
        "index.html",
        _payload
    )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def userlogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            return redirect('home')
    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def userlogout(request):
    logout(request)
    return redirect('home')


def home(request, query=None, _set=1, _limit=None, _order='title'):
    """
    Reset Search Queries & Return Home
    """
    _payload = payload(request, query, _set, _limit, _order, reset='1')
    return render(
        request,
        "index.html",
        _payload
    )


def show_collection(request, _collection, _colset):
    try:
        _set = int(_colset) + 1
    except Exception:
        _set = 1
    return render(
        request,
        "index.html",
        {
            "Books": collection(_collection, _set),
            "Set": str(_set),
            "Version": config.VERSION,
            "LeftNavCollections": menu("collections"),
            "LeftNav": menu("collections"),
            "Collections": collections_list(),
            "LeftNavMenu0": menu("nav_l_0"),
            "BookStats": Books.objects.all().count,
            "CollectionStats": Collections.objects.all().count,
            "CollectionObject": collections_list()
        },
    )


def flip_sort(request, bookset=1, query=None, _limit=None, _order='title'):
    """
    Goto next page in bookset
    """
    try: _set = int(bookset)
    except Exception: _set = 1
    _payload = payload(request, query, _set, _limit, _order, flip_sort=True)
    return render(
        request,
        "index.html",
        _payload,
    )


def next_page(request, bookset, query=None, _limit=None, _order='title'):
    """
    Goto next page in bookset
    """
    try:
        _set = int(bookset) + 1
    except Exception:
        _set = 1
    _payload = payload(request, query, _set, _limit, _order)
    return render(
        request,
        "index.html",
        _payload,
    )


def prev_page(request, bookset, query=None, _limit=None, _order='title'):
    """
    Goto previous page in bookset
    """
    _set = int(bookset)
    if _set <= 1:
        _set = 1
    else:
        try:
            _set = int(bookset) - 1
        except Exception:
            _set = 1
    _payload = payload(request, query, _set, _limit, _order)
    return render(
        request,
        "index.html",
        _payload,
    )


def book_set(_order, _limit=None, _set=1, _flip=False):
    """
    Get books results by set #
    """
    if _limit is None:
        _limit = 20  # TODO default from user choice
    _set_max = int(_set) * _limit
    _set_min = _set_max - _limit
    if _flip:
        books = Books.objects.all().order_by(_order).reverse()[_set_min:_set_max]
    else: 
        books = Books.objects.all().order_by(_order)[_set_min:_set_max]
    return books


def collection(_collection, _set, _limit=None):
    """
    Get books by collection id
    """
    _books = []
    books = []
    if _limit is None:
        _limit = 20
    _set_max = int(_set) * _limit
    _set_min = _set_max - _limit
    _collections = Collections.objects.filter(collection=_collection)
    for c in _collections:
        _books.append(c.book_id_id)
    return Books.objects.filter(id__in=_books)


def book_set_as_dict(_limit=None, _set=1):
    if _limit is None:
        _limit = 20
    _set_max = int(_set) * _limit
    _set_min = _set_max - _limit
    _set = {}
    for book in Books.objects.all()[_set_min:_set_max]:
        _set[book.title] = {
            "title": book.title,
            "author": book.author,
            "categories": book.categories,
            "cover": book.cover,
            "pages": book.pages,
            "progress": book.progress,
            "file_name": book.file_name,
            "pk": book.pk,
        }
    return json.dumps(_set)


def download(request, pk):
    """
    Download book by primary key
    """
    _book = Books.objects.all().filter(pk=pk)[0]
    _fn = hr_name(_book)
    response = HttpResponse(
        open(os.path.abspath(_book.file_name), "rb"), content_type="application/zip"
    )
    response["Content-Disposition"] = "attachment; filename=%s" % _fn
    return response


def favorite(request, pk):
    """
    Add book to favorites bu primary key
    """
    _book = Books.objects.all().filter(pk=pk)[0]
    print(Favorite(book=_book, uname=User))


def share(request, pk):
    """
    Share book by primary key
    """
    _book = Books.objects.all().filter(pk=pk)[0]
    _fn = hr_name(_book)
    response = HttpResponse(
        open(os.path.abspath(_book.file_name), "rb"), content_type="application/zip"
    )
    response["Content-Disposition"] = "attachment; filename=%s" % _fn
    return response


def info(request, pk):
    """
    Share book by primary key
    """
    _book = Books.objects.all().filter(pk=pk)[0]
    _fn = hr_name(_book)
    response = HttpResponse(
        open(os.path.abspath(_book.file_name), "rb"), content_type="application/zip"
    )
    response["Content-Disposition"] = "attachment; filename=%s" % _fn
    return response


def hr_name(book):
    """
    Nicer file names
    """
    return "{0}{1}".format(slugify(book.title), os.path.splitext(book.file_name)[1])


def format_list(list_in):
    formated_list, formated_list_key, x = [], [], 0
    for i in list_in:
        if i.id not in formated_list_key:
            if x % 2 == 0:
                c = 0
            else:
                c = 1
            if x <= 10:
                x += 1
            else:
                x = 0


def menu(which, _set=1, parent=None):
    if which == "collections":
        collection_list = collections
        _collections, collection_key, x = [], [], 0
        for i in collection_list:
            if i.collection not in collection_key:
                # Using c as the alternating row identifier
                # set c here
                if x % 2 == 0:
                    c = 0
                else:
                    c = 1
                if x <= 10:
                    x = x + 1
                else:
                    x = 0
                # TODO trim #'s and symbols from front of collection name
                if len(i.collection) > 16:
                    collection_string = i.collection[0:16] + " ..."
                else:
                    collection_string = i.collection

                _collections.append(
                    {"string": collection_string, "link": i.collection, "class": c}
                )
                collection_key.append(i.collection)
        return _collections
    elif which == "nav_lvl_0":
        navigation_list = Navigation.objects.all()
        return navigation_list


def collections_list():
    collection_key = []
    for i in collections:
        if i.collection not in collection_key:
            collection_key.append(i.collection)
    return json.dumps(list(set(collection_key)))


def payload(request, query, _set, _limit, _order, **kwargs):
    """
    Return formatted data to template
    : notes : This is the least pythonic function I have ever written, but its
    still beautiful
    """
    try: request.session['ascending']
    except KeyError: request.session['ascending'] = True
    try:
        if kwargs['flip_sort']:
            request.session['ascending'] = not request.session['ascending']
    except KeyError: pass
    try:
        if kwargs['reset']:
            request.session['cached_query'] = query
            if _set < 1: _set = 1
            if _limit is None: _limit = 20
            _set_max = int(_set) * _limit
            _set_min = _set_max - _limit
            _now_showing = "%s-%s"%(_set_min, _set_max)
            if request.session['ascending']:
                _r = book_set(_order, _limit, _set)
            else: _r = book_set(_order, _limit, _set, True)
            _r_len, _search = None, None
    except KeyError:
        _set = int(_set)
        if _set < 1: _set = 1
        if _limit is None: _limit = 20
        _set_max = int(_set) * _limit
        _set_min = _set_max - _limit
        _now_showing = "%s-%s"%(_set_min, _set_max)
        if query: 
            if query != request.session.get('cached_query'):
                request.session['cached_query'] = query
                if request.session['ascending']:
                    _results = Books().generic_search(query)
                else: _results = Books().generic_search(query).reverse()
                _r, _r_len = \
                    _results[_set_min:_set_max],\
                    _results.count()
            elif query == request.session.get('cached_query'):
                if request.session['ascending']:
                    _results = Books().generic_search(query)
                else: _results = Books().generic_search(query).reverse()
                _r, _r_len = \
                    _results.order_by(_order)[_set_min:_set_max],\
                    _results.count()
        else:
            try:
                query = request.session['cached_query']  # Is there a cached query?
                if query == None: raise KeyError
                if request.session['ascending']:
                    _results = Books().generic_search(query)
                else: _results = Books().generic_search(query).reverse()
                _r, _r_len = \
                    _results.order_by(_order)[_set_min:_set_max],\
                    _results.count()
            except KeyError:
                if request.session['ascending']:
                    _r = book_set(_order, _limit, _set)
                else: _r = book_set(_order, _limit, _set, True)
                _r_len, _search = None, None
    
    _bookstats, _collectionstats, _collectionobject = \
        Books.objects.all().count(), Collections.objects.all().count(), \
        collections_list()
    if (_r_len): _btotal = str(_r_len)
    else: _btotal = str(_bookstats)
    
    return {
        "Books": _r,
        "Set": str(_set),
        "Version": config.VERSION,
        "LeftNavCollections": menu("collections"),
        "LeftNavMenu0": menu("nav_l_0"),
        "BookStats": _btotal,
        "CollectionStats": _collectionstats,
        "CollectionObject": _collectionobject,
        "NowShowing": _now_showing,
        "PostedSearch": query,
        "SearchLen": _r_len,
        "Order": _order,
    }

