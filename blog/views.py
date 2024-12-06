from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Article, Tag, Comment
from .forms import CommentForm, CommentReplyForm

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
        return render(request,
                    "blog/detail.html",
                    {"article": self.article_instance,
                     "comments":comments,
                     "form":self.form_class,
                     "reply_form": self.form_class_reply})

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