from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify

from .models import Article, Tag, Comment, Vote
from .forms import CommentForm, CommentReplyForm, ArticlesEditForm

class ArticleView(View):
    def get(self, request, tag_slug=None):
            articles = Article.published.all()
            if tag_slug:
                tag = get_object_or_404(Tag, slug=tag_slug)
                articles = articles.filter(tags__in=[tag])
            return render(request, "blog/articles.html", {"articles": articles})

class DetailView(View):
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.article_instance = get_object_or_404(Article, status=Article.Status.PUBLISHED,
                            publish__year=kwargs["year"],
                            publish__month=kwargs["month"],
                            publish__day=kwargs["day"],
                            slug=kwargs["slug"],)
        return super().setup(request, *args, **kwargs)

    def get(self, request, year, month, day, slug):
        comments = self.article_instance.comments.filter(active=True)
        can_like = False
        if request.user.is_authenticated and self.article_instance.user_can_like(request.user):
            can_like = True
        return render(request,
                    "blog/detail.html",
                    {"article": self.article_instance,
                     "comments":comments,
                     "form":self.form_class,
                     "reply_form": self.form_class_reply,
                     "can_like": can_like,})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.article = self.article_instance
            new_comment.save()
            messages.success(request, "your comment submitted successfully", "success")
            return redirect(self.article_instance.get_absolute_url())


        else:
            messages.error(request, "There was an error submitting your comment.", "error")
            return render(request, "blog/detail.html", {
                "article": self.article_instance,
                "comments": self.article_instance.comments.filter(active=True),
                "form": form,
            })

class ArticleAddReplyView(LoginRequiredMixin, View):
	form_class = CommentReplyForm

	def post(self, request, article_id, comment_id):
		article = get_object_or_404(Article, id=article_id)
		comment = get_object_or_404(Comment, id=comment_id)
		form = self.form_class(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.user = request.user
			reply.article = article
			reply.reply = comment
			reply.is_reply = True
			reply.save()
			messages.success(request, "your reply submitted successfully", "success")
		return redirect(article.get_absolute_url())

class ArticleLikeView(LoginRequiredMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        like = Vote.objects.filter(user=request.user, article=article)
        if like.exists():
            messages.error(request, "You have already liked this post", "error")
        else:
            Vote.objects.create(user=request.user, article=article)
            messages.success(request, "You liked this post", "success")
        return redirect(article.get_absolute_url())

class ArticleEditView(LoginRequiredMixin, View):
    form_class = ArticlesEditForm
    template_name = "blog/edit.html"

    def setup(self, request, *args, **kwargs):
        self.article_instance = get_object_or_404(Article, status=Article.Status.PUBLISHED,
                            publish__year=kwargs["year"],
                            publish__month=kwargs["month"],
                            publish__day=kwargs["day"],
                            slug=kwargs["slug"],)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        article = self.article_instance
        if not article.author.id == request.user.id:
            messages.error(request, "you cant update this post", "danger")
            return redirect("blog:home")
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        article = self.article_instance
        form = self.form_class(instance=article)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        article = self.article_instance
        form = self.form_class(request.POST, instance=article)
        if form.is_valid():
            update_article = form.save(commit=False)
            update_article.slug = slugify(form.cleaned_data["title"])
            update_article.save()
            messages.success(request, "you updated this post", "success")
            return redirect(article.get_absolute_url())

class ArticleDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, status=Article.Status.PUBLISHED,
                            publish__year=kwargs["year"],
                            publish__month=kwargs["month"],
                            publish__day=kwargs["day"],
                            slug=kwargs["slug"],)
        if article.author.id == request.user.id:
            article.delete()
            messages.success(request, "post deleted successfully", "success")
        else:
            messages.error(request, "you cant delete this post", "danger")
        return redirect("accounts:user_profile")