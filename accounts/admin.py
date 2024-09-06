from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "phone_number", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields":("email", "phone_number", "password")}),
        ("Permissions", {"fields":("is_active", "is_admin", "last_login")}),
    )

    add_fieldsets = (
        (None, {"fields":("email", "phone_number", "surname", "forename", "password", "confirm_password")}),
    )
    search_fields = ("email", "surname", "forename")
    ordering = ("surname",)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)