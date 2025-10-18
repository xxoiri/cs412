# mini_insta/admin.py
# register models for admin usage
# by Amy Ho, aho@bu.edu

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo, Follow
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)