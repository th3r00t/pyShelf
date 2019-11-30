import json
import os
from base64 import b64decode, b64encode

from django.db import models
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, render_to_response
from django.utils.text import slugify

from .models import Books


def index(request):
    _set = 1
    return render(
        request, "index.html", {"Books": book_set(20, _set), "Set": str(_set)}
    )


def next_page(request, bookset):
    try:
        _set = int(bookset) + 1
    except Exception:
        _set = 1
    return render(
        request, "index.html", {"Books": book_set(None, _set), "Set": str(_set)}
    )


def prev_page(request, bookset):
    _set = int(bookset)
    if _set <= 1:
        _set = 1
    else:
        try:
            _set = int(bookset) - 1
        except Exception:
            _set = 1
    return render(
        request, "index.html", {"Books": book_set(None, _set), "Set": str(_set)}
    )


def book_set(_limit=None, _set=1):
    if _limit is None:
        _limit = 20  # TODO default from user choice
    _set_max = int(_set) * _limit
    _set_min = _set_max - _limit
    books = Books.objects.all()[_set_min:_set_max]
    return books


def book_set_as_dict(_limit=None, _set=1):
    breakpoint()
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
    _book = Books.objects.all().filter(pk=pk)[0]
    _fn = hr_name(_book)
    response = HttpResponse(
        open(os.path.abspath(_book.file_name), "rb"), content_type="application/zip"
    )
    response["Content-Disposition"] = "attachment; filename=%s" % _fn
    return response


def hr_name(book):
    return "{0}.{1}".format(slugify(book.title), book.file_name.split(".")[1])
