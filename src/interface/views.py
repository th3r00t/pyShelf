import os

from django.shortcuts import HttpResponse, render
from django.utils.text import slugify

from .models import Books


def index(request):
    return render(request, "index.html", {"Books": Books.objects.all()})


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


def book_set(_set):
    r = 20
    x = _set * r
    y = x + r
    books = Books.objects.all()[x:y]
    return books
