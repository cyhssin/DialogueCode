from django.shortcuts import render, get_object_or_404
from django.views import View


from .models import Article, Category, Tag

class ArticleView(View):
    def get(self, request, tag_slug=None):
            articles = Article.published.all()
            if tag_slug:
                tag = get_object_or_404(Tag, slug=tag_slug)
                articles = articles.filter(tags__in=[tag])
            return render(request, "blog/articles.html", {"articles": articles})