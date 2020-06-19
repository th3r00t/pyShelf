import json
import os
from base64 import b64decode, b64encode
from pathlib import Path

from backend.lib.config import Config
from django.db import models
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render  # render_to_response
from django.utils.text import slugify

from .models import Books, Collections, Navigation

config = Config(Path("../"))


def index(request):
    """
    Return template index
    """
    _set = 1
    return render(
        request,
        "index.html",
        {
            "Books": book_set(20, _set),
            "Set": str(_set),
            "Version": config.VERSION,
            "LeftNavCollections": menu("collections"),
            "LeftNavMenu0": menu("nav_l_0"),
        },
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
        },
    )


def next_page(request, bookset):
    """
    Goto next page in bookset
    """
    try:
        _set = int(bookset) + 1
    except Exception:
        _set = 1
    return render(
        request,
        "index.html",
        {
            "Books": book_set(None, _set),
            "Set": str(_set),
            "Version": config.VERSION,
            "LeftNavCollections": menu("collections"),
            "LeftNav": menu("collections"),
        },
    )


def prev_page(request, bookset):
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
    return render(
        request,
        "index.html",
        {
            "Books": book_set(None, _set),
            "Set": str(_set),
            "Version": config.VERSION,
            "LeftNavCollections": menu("collections"),
            "LeftNav": menu("collections"),
        },
    )


def search(request, query=None, _set=1, _limit=None):
    """
    Call generic search and return rendered results
    """
    _set = int(_set)
    if query is None:
        return render(request, "index.html", {"Books": None, "Version": config.VERSION})
    if _limit is None:
        _limit = 20  ## TODO set to user defaults
    if _set < 1:
        _set = 1
    _set_max = int(_set) * _limit
    _set_min = _set_max - _limit
    search = Books().generic_search(query)
    search_len = search.count()
    _r = search[_set_min:_set_max]
    return render(
        request,
        "search.html",
        {
            "Books": _r,
            "Query": query,
            "Set": _set,
            "len_results": search_len,
            "Version": config.VERSION,
            "LeftNavCollections": menu("collections"),
            "LeftNav": menu("collections"),
        },
    )


def book_set(_limit=None, _set=1):
    """
    Get books results by set #
    """
    if _limit is None:
        _limit = 20  # TODO default from user choice
    _set_max = int(_set) * _limit
    _set_min = _set_max - _limit
    books = Books.objects.all()[_set_min:_set_max]
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
    Favorite book by primary key
    """
    _book = Books.objects.all().filter(pk=pk)[0]
    _fn = hr_name(_book)
    response = HttpResponse(
        open(os.path.abspath(_book.file_name), "rb"), content_type="application/zip"
    )
    response["Content-Disposition"] = "attachment; filename=%s" % _fn
    return response

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
        collection_list = Collections.objects.all()
        collections, collection_key, x = [], [], 0
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

                collections.append(
                    {"string": collection_string, "link": i.collection, "class": c}
                )
                collection_key.append(i.collection)
        return collections
    elif which == "nav_lvl_0":
        navigation_list = Navigation.objects.all()
        breakpoint()
        return navigation_list
