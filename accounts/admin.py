from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Profile, OtpCode

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
	list_display = ["phone_number", "code", "created"]

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ["email", "phone_number", "is_admin"]
	list_filter = ["is_admin"]
	readonly_fields = ["last_login"]

	fieldsets = (
		("Main", {"fields":("email", "phone_number", "sur_name", "for_name", "password")}),
		("Permissions", {"fields":("is_active", "is_admin", "is_superuser", "last_login", "groups", "user_permissions")}),
	)

	add_fieldsets = (
		(None, {"fields":("phone_number", "email", "sur_name", "for_name", "password1", "password2")}),
	)

	search_fields = ["email", "sur_name", "for_name"]
	ordering = ["for_name"]
	filter_horizontal = ["groups", "user_permissions"]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser
		if not is_superuser:
			form.base_fields["is_superuser"].disabled = True
		return form

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False

class ExtendedUserAdmin(UserAdmin):
	inlines = (ProfileInline,)

# Register the custom User admin
admin.site.register(User, ExtendedUserAdmin)