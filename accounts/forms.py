from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields  = ("phone_number", "email", "sur_name", "fore_name")

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd["password"] and cd["confirm_password"] and cd["password"] != cd["confirm_password"]:
            raise ValidationError("Passwords don`t match")
        return cd["confirm_password"]
    
    # override Save Function for hash password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">"
                                        "this form</a>.")

    class Meta:
        model = User
        fields = ("phone_number", "email", "sur_name", "fore_name", "password", "last_login")


class UserRegisterForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(label="Phone Number")
    password = forms.CharField(widget=forms.PasswordInput)

    def email_clean(self):
        email = self.cleaned_data["email"]
        user = User.objects.get(email=email).exists()
        if user:
            raise ValidationError("This Email Already exists.")
        return email

    def phone_clean(self):
        phone = self.cleaned_data["phone"]
        user = User.objects.get(phone_number=phone).exists()
        if user:
            raise ValidationError("This Phone Already Exists")
        return phone