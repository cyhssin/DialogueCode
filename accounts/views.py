from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegistrationForm

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session["user_registration_info"] = {
                "email": form.cleaned_data["email"],
                "phone": form.cleaned_data["phone"],
                "sur_name": form.cleaned_data["sur_name"],
                "for_name": form.cleaned_data["for_name"],
                "password": form.cleaned_data["password"],
            }
            return redirect("blog:home")
        return render(request, self.template_name, {"form": form})
