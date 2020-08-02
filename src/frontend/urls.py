"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.urls import include, path, re_path
from interface import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    re_path("^live$", views.live, name="live"),
    path("sort/<_order>", views.index, name="index"),
    path("flip_sort/<_order>", views.flip_sort, name="index"),
    path("download/<pk>", views.download, name="download"),
    path("share/<pk>", views.share, name="share"),
    path("share/<pk>", views.info, name="info"),
    path("prev_page/<bookset>", views.prev_page, name="prev_page"),
    path("next_page/<bookset>", views.next_page, name="next_page"),
    path("prev_page/<bookset>/<_order>", views.prev_page, name="prev_page"),
    path("next_page/<bookset>/<_order>", views.next_page, name="next_page"),
    path("search/", views.index, name="search"),
    path("search/<query>", views.index, name="search"),
    path("search/<query>/<_set>", views.index, name="search"),
    path("collections", views.collectionspage, name="collections"),
    path("show_collection/<query>/<_set>", views.show_collection, name="show_collection"),
    path("signup", views.signup, name="signup"),
    path("login", views.userlogin, name="login"),
    path('logout', views.userlogout, name='logout'),
    path('favorite/<pk>', views.favorite, name='favorite'),
    path('favorites', views.favorites, name='favorites'),
    path('favorites/<bookset>', views.favorites, name='favorites'),
    path('favorites/<bookset>/<query>', views.favorites, name='favorites'),
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
