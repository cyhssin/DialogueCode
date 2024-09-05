from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    

class PublishManager(models.Manager):
    # Custom manager to filter published posts
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

 
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    thumbnail = models.ImageField(blank=True, null=True )
    description = models.TextField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishManager()

    def __str__(self):
        return f"{self.title} - {self.author} - {self.created}"
    
    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
            ]
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")

    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])
    

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        verbose_name = ("comment")
        verbose_name_plural = ("Comments")
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"