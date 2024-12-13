from django import forms

from .models import Comment, Article

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["title", "description"]

class CommentReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ("description",)

class ArticlesEditForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ["title", "description", "slug", "category", "tags"]