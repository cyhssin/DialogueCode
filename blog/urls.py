from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
]
