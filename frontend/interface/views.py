import xsendfile
from django.shortcuts import render

from .models import Books


def index(request):
    return render(request, "index.html", {"Books": Books.objects.all()})


def download(request, pk):
    _fp = Books.objects.all().filter(pk=pk)[0].file_name
    return xsendfile.XSendfile('"' + _fp + '"')


def book_set(_set):
    r = 20
    x = _set * r
    y = x + r
    books = Books.objects.all()[x:y]
    return books
