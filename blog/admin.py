from django.contrib import admin
from .models import Article, Category, Tag, FavoriteArticle, Comment, Vote

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_select_related = ["author", "category"]
    list_display = ["title", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug":("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ["owner"]
    list_display = ["title", "created"]
    list_filter = ["owner", "created"]
    prepopulated_fields = {"slug":("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_select_related = ["owner"]
    list_display = ["title", "created"]
    list_filter = ["owner", "created"]
    prepopulated_fields = {"slug":("title",)}

@admin.register(FavoriteArticle)
class FavoriteArticleAdmin(admin.ModelAdmin):
    list_select_related = ["user", "article"]
    list_display = ["created"]
    list_filter = ["user", "article"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_select_related = ["user", "article"]
    list_display = ["created"]
    list_filter = ["user", "article"]

admin.site.register(Vote)