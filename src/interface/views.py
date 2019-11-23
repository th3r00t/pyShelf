import os

from django.db import models
from django.shortcuts import HttpResponse, render
from django.utils.text import slugify

from .models import Books


def index(request):
    return render(request, "index.html", {"Books": book_set()})
    # return render(request, "index.html", {"Books": Books.objects.all()})


def book_set(_limit=None, _set=1):
    if _limit is None:
        _limit = 20  # TODO default from user choice
    _set_max = _set * _limit
    _set_min = _set_max - _limit
    books = Books.objects.all()[_set_min:_set_max]
    return books


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
