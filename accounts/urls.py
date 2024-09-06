from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView        

from . import views
app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
]       