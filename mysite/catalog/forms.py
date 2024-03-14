from django.forms import ModelForm
from .models import Comment


class AddNewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['review_text', 'grade']