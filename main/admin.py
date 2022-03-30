from django.contrib import admin
from .models import Category, Post, Comment, Author, PostCategory

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(PostCategory)

# Register your models here.
