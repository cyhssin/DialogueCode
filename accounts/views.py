import random
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .forms import UserRegistrationForm, UserProfileForm, UserLoginForm, VerifyCodeForm
from .models import User, Profile, OtpCode
from utils import send_otp_code

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data["phone"], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data["phone"], code=random_code)
            request.session["user_registration_info"] = {
                "email": form.cleaned_data["email"],
                "phone": form.cleaned_data["phone"],
                "sur_name": form.cleaned_data["sur_name"],
                "for_name": form.cleaned_data["for_name"],
                "password": form.cleaned_data["password"],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect("accounts:verify_code")
        return render(request, self.template_name, {"form": form})

class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/verify_code.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user_session = request.session["user_registration_info"]
        code_instance = OtpCode.objects.get(phone_number=user_session["phone"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["code"] == code_instance.code:
                User.objects.create_user(user_session["phone"], user_session["email"],
										 user_session["sur_name"], user_session["for_name"], user_session["password"])
                code_instance.delete()
                messages.success(request, "You registered.", "success")
                return redirect("blog:home")
            else:
                messages.error(request, "this code is wrong", "danger")
                return redirect("accounts:verify_code")
        return redirect("blog:home")


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