from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["title", "description"]

class CommentReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ("description",)