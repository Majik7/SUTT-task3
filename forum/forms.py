from django import forms
from .models import Post, Reply, Report

class replyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

class reportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']

class postForm(forms.ModelForm):
    tags_input = forms.CharField(
        label="Tags (Separated by commas)",
        required=False,
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'course', 'tags_input']