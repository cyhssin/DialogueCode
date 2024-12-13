from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.ArticleView.as_view(), name="home"),
    path("tag/<slug:tag_slug>/", views.ArticleView.as_view(), name="article_list_by_tag"),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", views.DetailView.as_view(), name="article_detail"),
    path("reply/<int:article_id>/<int:comment_id>/", views.ArticleAddReplyView.as_view(), name="add_reply"),
	path("like/<int:article_id>/", views.ArticleLikeView.as_view(), name="article_like"),
	path("edit/<int:year>/<int:month>/<int:day>/<slug:slug>/", views.ArticleEditView.as_view(), name="article_edit"),
	path("delete/<int:year>/<int:month>/<int:day>/<slug:slug>/", views.ArticleDeleteView.as_view(), name="article_delete"),

]
