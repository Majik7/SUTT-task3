from django import forms
from .models import Post, Reply

class replyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']