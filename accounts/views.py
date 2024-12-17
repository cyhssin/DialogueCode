from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .forms import UserRegistrationForm, UserProfileForm, UserLoginForm
from .models import User, Profile

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
            session = request.session["user_registration_info"]
            User.objects.create_user(session["phone"], session["email"], session["sur_name"],
                                                        session["for_name"], session["password"],)
            return redirect("accounts:user_profile")
        return render(request, self.template_name, {"form": form})

class ProfileUserView(LoginRequiredMixin, View):
    form_class = UserProfileForm
    template_name = "accounts/profile.html"

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        articles = user.articles.all()
        profile = get_object_or_404(Profile, user=user)
        form = self.form_class(instance=profile, initial={"email": request.user.email})
        age = profile.get_age()
        return render(request, self.template_name, {"user": user,
                                        "articles": articles, "form": form, "age": age})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            messages.success(request, "profile edited successfully", "success")
        return redirect("accounts:user_profile", request.user.id)

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/user_login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd["phone"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "You logged in successfully", "info")
            return redirect("blog:home")
        messages.error(request, "Email or password is wrong", "warning")
        return render(request, self.template_name, {"form":form})

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You logged out successfully", "success")
        return redirect("blog:home")