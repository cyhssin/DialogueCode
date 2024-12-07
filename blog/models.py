from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

User = settings.AUTH_USER_MODEL

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

    def likes_count(self):
        return self.pvotes.count()

    def user_can_like(self, user):
        user_like = user.uvotes.filter(article=self)
        if user_like.exists():
            return True
        return False

    def get_absolute_url(self):
        return reverse("blog:article_detail",
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug,
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

class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_article")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="favorite_by")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article")   # Ensure a user can favorite an article only

    def __str__(self) -> str:
        return f"{self.user.username} - {self.article.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_by")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    reply = models.ForeignKey("self", on_delete=models.CASCADE, related_name="rcomments", blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.user} on {self.article}"

class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvotes")
	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="pvotes")

	def __str__(self):
		return f"{self.user} liked {self.article.slug}"