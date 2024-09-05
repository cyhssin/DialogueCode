import random
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


from .forms import UserRegisterForm
from .models import User


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = "accounts/register_page.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session["user_registration_info"] = {
                "phone_number": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "full_name": form.cleaned_data["full_name"],
                "password": form.cleaned_data["password"],
            }
            return redirect("accounts:verify_code")
        return render(request, self.template_name, {"form":form})