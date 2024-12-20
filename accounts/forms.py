from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Profile
from blog.models import Article

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("email", "phone_number", "sur_name", "for_name")

	def clean_password2(self):
		cd = self.cleaned_data
		if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
			raise ValidationError("Passwords dont match")
		return cd["password2"]

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserRegistrationForm(forms.Form):
	email = forms.EmailField()
	phone = forms.CharField(max_length=11)
	sur_name = forms.CharField(label="sur_name")
	for_name = forms.CharField(label="for_name")
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_email(self):
		email = self.cleaned_data["email"]
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError("This email already exists")
		return email

	def clean_phone(self):
		phone = self.cleaned_data["phone"]
		user = User.objects.filter(phone_number=phone).exists()
		if user:
			raise ValidationError("This phone number already exists")
		return phone

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form</a>.")

	class Meta:
		model = User
		fields = ("email", "phone_number", "sur_name", "for_name", "password", "last_login")
	
class UserProfileForm(forms.ModelForm):
	email = forms.EmailField()
	
	class Meta:
		model = Profile
		fields = ["birth", "bio"]


class UserLoginForm(forms.Form):
	phone = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class VerifyCodeForm(forms.Form):
	code = forms.IntegerField()