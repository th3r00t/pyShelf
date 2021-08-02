from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin

from .models import Books, Collections, Favorites, Navigation, User
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ["email", "username", "facebook", "twitter", "sponsorid", "matrixid"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ()}),
        ("Personal info", {"fields": ("facebook", "twitter", "matrixid")}),
        ("Permissions", {"fields": ("sponsorid",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"classes": ("wide",), "fields": ("facebook", "twitter", "sponsorid", "matrixid")},),
    )

class pyShelfAdminSite(AdminSite):
    site_title = 'pyShelf admin'
    site_header = 'pyShelf Administration'
    index_title = 'Library'


admin_site = pyShelfAdminSite(name='pyadmin')
admin_site.register(Books)
admin_site.register(Collections)
admin_site.register(Favorites)
admin_site.register(Navigation)
admin_site.register(User, CustomUserAdmin)
