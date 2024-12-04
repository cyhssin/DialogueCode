from django.contrib import admin
from .models import Article, Category, Tag, FavoriteArticle, Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug":("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "created"]
    list_filter = ["owner", "created"]
    prepopulated_fields = {"slug":("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "created"]
    list_filter = ["owner", "created"]
    prepopulated_fields = {"slug":("title",)}

@admin.register(FavoriteArticle)
class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ["user", "article", "created"]
    list_filter = ["user", "article"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "article", "created"]
    list_filter = ["user", "article"]
