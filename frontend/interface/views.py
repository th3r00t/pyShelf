from django.shortcuts import render
from xsendfile import XSendfileApplication

from .models import Books


def index(request):
    return render(request, "index.html", {"Books": Books.objects.all()})


def download(request):
    return XSendfileApplication(file_name)


def book_set(_set):
    r = 20
    x = _set * r
    y = x + r
    books = Books.objects.all()[x:y]
    return books
