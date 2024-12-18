from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
	path("register/", views.UserRegistrationView.as_view(), name="user_register"),
	path("verify/", views.UserRegisterVerifyCodeView.as_view(), name="verify_code"),
	path("profile/<int:user_id>/", views.ProfileUserView.as_view(), name="user_profile"),
	path("login/", views.UserLoginView.as_view(), name="user_login"),
	path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
]