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