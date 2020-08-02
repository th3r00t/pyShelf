from django.contrib import admin
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


admin.site.register(Books)
admin.site.register(Collections)
admin.site.register(Favorites)
admin.site.register(Navigation)
admin.site.register(User, CustomUserAdmin)
