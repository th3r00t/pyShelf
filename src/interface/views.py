import json
import os
from base64 import b64decode, b64encode
from pathlib import Path

from backend.lib.config import Config
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render  # render_to_response
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.text import slugify

from .forms import SignUpForm, UserLoginForm
from .models import Books, Collections, Favorites, Navigation, User

config = Config(Path("../"))



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


def favorites(request, query=None, _set=1, _limit=None, _order='title'):
    """
    Return template index
    """
    _payload = payload(request, query, _set, _limit, _order, favorites=True, reset=True)
    return render(
        request,
        "index.html",
        _payload
    )


def collectionspage(request):

    pass


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
            user.save()
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
    _payload = payload(request, query, _set, _limit, _order, reset=True)
    return render(
        request,
        "index.html",
        _payload
    )


def show_collection(request, query, _set, _limit=None, _order='title', **kwargs):
    try:
        _set = int(_set) + 1
    except Exception:
        _set = 1

    _set = int(_set)  # Get set #
    if _set < 1: _set = 1  # If there is no set data, set = 1
    if _limit is None: _limit = 20  # If we havent set limit limit = 20
    _set_max = int(_set) * _limit  # Multiply current set by limit to get upper limits
    _set_min = _set_max - _limit  #  Subtract limiter to get bottom limit
    _now_showing = "%s-%s"%(_set_min, _set_max)  # Set the set count
    if query:  # Are we sending a query?
        if query != request.session.get('cached_query'):  # Is it different to the last query?
            request.session['cached_query'] = query  # Set the session data to track the query
            if request.session['ascending']:
                _r = _results = Collections().generic_search(query)  # Get the query, or in reverse below
            else: _results = Collections().generic_search(query).reverse()
            _r, _r_len = \
                _results[_set_min:_set_max],\
                len(_results)
        elif query == request.session.get('cached_query'):  # The queries are equal check the direction
            if request.session['ascending']:
                _results = Collections().generic_search(query)
            else: _results = Collections().generic_search(query).reverse()
            _r, _r_len = \
                _results.order_by(_order)[_set_min:_set_max],\
                len(_results)
    else:
        try:
            query = request.session['cached_query']  # Is there a cached query?
            if query == None: raise KeyError
            if request.session['ascending']:
                _results = Collections().generic_search(query)
            else: _results = Collections().generic_search(query).reverse()
            _r, _r_len = \
                _results.order_by(_order)[_set_min:_set_max],\
                len(_results)
        except KeyError:
            if request.session['ascending']:
                _r = book_set(request, _order, _limit, _set, False, **kwargs)
            else: _r = book_set(request, _order, _limit, _set, True, **kwargs)
            _r_len, _search = None, None

    _bookstats = len(Collections().generic_search(query))
    if (_r_len): _btotal = str(_r_len)
    else: _btotal = str(_bookstats)
    
    return render(
       request,
       "index.html",
        {
            "Books": _results,
            "Set": str(_set),
            "Version": config.VERSION,
            # "LeftNavCollections": menu("collections"),
            # "LeftNavMenu0": menu("nav_l_0"),
            "BookStats": _btotal,
            "CollectionStats": Collections.objects.all().count(),
            "CollectionObject": collections_list,
            "NowShowing": _now_showing,
            "PostedSearch": query,
            "SearchLen": _r_len,
            "Order": _order,
        })


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


def book_set(request, _order, _limit=None, _set=1, _flip=False, **kwargs):
    """
    Get books results by set #
    """
    try:
        book_key = []
        if kwargs['favorites'] is True:
            for id in Favorites.objects.all().filter(user=request.user):
                book_key.append(id.book.id)
            BookObject = Books.objects.filter(id__in=(book_key))
    except KeyError: BookObject = Books.objects.all()
    if _limit is None:
        _limit = 20  # TODO default from user choice
    _set_max = int(_set) * _limit
    _set_min = _set_max - _limit
    if _flip:
        books = BookObject.order_by(_order).reverse()[_set_min:_set_max]
    else: 
        books = BookObject.order_by(_order)[_set_min:_set_max]
    return mark_favorites(request, books)


def mark_favorites(request, bookset):
    try:
        favorites = Favorites.objects.filter(user=request.user)
        for book in bookset:
            for favorite in favorites:
                if book == favorite.book:
                    book.is_favorite = True
                    pass
        return bookset
    except Exception as e:
        for book in bookset:
            book.if_favorite = False
    return bookset


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


def download(request, pk):
    """
    Download book by primary key
    """
    _book = Books.objects.get(pk=pk)
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
    try:
        _d = Favorites.objects.filter(user=request.user, book=Books.objects.get(pk=pk))
    except TypeError as e:
        return redirect('login')
    if len(_d) == 1:
        _d.delete()
        return HttpResponse(status=204)
    _f = Favorites(book=Books.objects.get(pk=pk))
    _f.user = request.user
    _f.save()
    return HttpResponse(status=204)


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
        _collections_list = Collections.objects.all()
        _collections, collection_key, x = [], [], 0
        for i in _collections_list:
            if i.collection not in collection_key:
                if x % 2 == 0: c = 0
                else: c = 1
                if x <= 10: x = x + 1
                else: x = 0
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
    collections = Collections.objects.all()
    collection_key = []
    for i in collections:
        if i.collection not in collection_key:
            collection_key.append(i.collection)
    return list(set(collection_key))


def live(request, **kwargs):
    """
    Respond to live requests. Primarily used as a response object for Ajax calls
    :param GET['hook']: collection_listing, book_details, register
    :param kwargs['pk']: Primary key of requested object
    :return: JsonResponse Object, status response code
    """
    err_txt = {"err": "There is no responder for your request"}
    try: hook = request.GET['hook']
    except MultiValueDictKeyError as e: return JsonResponse(err_txt, status=404)

    if hook == "collection_listing":
        collections = collections_list()
        return JsonResponse({"data": collections}, status=200)
    elif hook == "details":
        try: _pk = request.GET['pk']
        except KeyError as e: return False
        book = book_details(Books.objects.get(pk=_pk))
        return JsonResponse({"data": book}, status=200)
    elif hook == "register":
        html = render_to_string('signup.html', {'form': SignUpForm}, request)
        html += render_to_string('login.html', {'form': UserLoginForm}, request)
        return JsonResponse({"data": html})
    else: return JsonResponse(err_txt, status=404)

    return JsonResponse({"data": "Response sent"}, status=200)

def book_details(book):
    return {
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'tags': book.tags,
        'rights': book.rights,
        'pk': book.id
    }
def payload(request, query, _set, _limit, _order, **kwargs):
    """
    Return formatted data to template
    : notes : This is the least pythonic function I have ever written, but its
    still beautiful
    """
    try: request.session['ascending']
    except KeyError: request.session['ascending'] = True
    try:  # Are we fliping the sort?
        if kwargs['flip_sort']:
            request.session['ascending'] = not request.session['ascending']
    except KeyError: pass
    try:  # Are we resetting the session?
        if kwargs['reset']:
            request.session['cached_query'] = query
            if _set < 1: _set = 1
            if _limit is None: _limit = 20
            _set_max = int(_set) * _limit
            _set_min = _set_max - _limit
            _now_showing = "%s-%s"%(_set_min, _set_max)
            if request.session['ascending']:
                _r = book_set(request, _order, _limit, _set, False, **kwargs)
            else: _r = book_set(request, _order, _limit, _set, True, **kwargs)
            _r_len, _search = None, None
    except KeyError:
        _set = int(_set)  # Get set #
        if _set < 1: _set = 1  # If there is no set data, set = 1
        if _limit is None: _limit = 20  # If we havent set limit limit = 20
        _set_max = int(_set) * _limit  # Multiply current set by limit to get upper limits
        _set_min = _set_max - _limit  #  Subtract limiter to get bottom limit
        _now_showing = "%s-%s"%(_set_min, _set_max)  # Set the set count
        if query:  # Are we sending a query?
            if query != request.session.get('cached_query'):  # Is it differnt to the last query?
                request.session['cached_query'] = query  # Set the session data to track the query
                if request.session['ascending']:
                    _results = Books().generic_search(query)  # Get the query, or in reverse below
                else: _results = Books().generic_search(query).reverse()
                _r, _r_len = \
                    _results[_set_min:_set_max],\
                    _results.count()
            elif query == request.session.get('cached_query'):  # The queries are equal check the direction
                if request.session['ascending']:
                    _results = Books().generic_search(query)
                else: _results = Books().generic_search(query).reverse()
                _r, _r_len = \
                    _results.order_by(_order)[_set_min:_set_max],\
                    _results.count()
        else:  # No new query was passed
            try:
                query = request.session['cached_query']  # Is there a cached query?
                if query == None: raise KeyError  # No cached query exists jump to KeyError
                if request.session['ascending']:
                    _results = Books().generic_search(query)
                else: _results = Books().generic_search(query).reverse()
                _r, _r_len = \
                    _results.order_by(_order)[_set_min:_set_max],\
                    _results.count()
            except KeyError:
                if request.session['ascending']:
                    _r = book_set(request, _order, _limit, _set, False, **kwargs)
                else: _r = book_set(request, _order, _limit, _set, True, **kwargs)
                _r_len, _search = None, None
    
    _bookstats = Books.objects.all().count()
    if (_r_len): _btotal = str(_r_len)
    else: _btotal = str(_bookstats)
    # Format the payload and return it to the view
    return {
        "Books": _r,
        "Set": str(_set),
        "Version": config.VERSION,
        # "LeftNavCollections": menu("collections"),
        # "LeftNavMenu0": menu("nav_l_0"),
        "BookStats": _btotal,
        "CollectionStats": Collections.objects.all().count(),
        "CollectionObject": collections_list,
        "NowShowing": _now_showing,
        "PostedSearch": query,
        "SearchLen": _r_len,
        "Order": _order,
    }
