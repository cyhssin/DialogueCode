from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class PublishManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Article.Status.PUBLISHED)

class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="media/products/%Y/%m/%d", blank=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category")
    tags = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tags")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    publish = models.DateTimeField(default=timezone.now, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
            ]
        verbose_name = "Article"
        verbose_name_plural = "Articles"


    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:article_detail",
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])

class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=75)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    title = models.CharField(max_length=75)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return self.title