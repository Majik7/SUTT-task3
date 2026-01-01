from django.contrib import admin
from .models import Category, Post, Report

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Report)