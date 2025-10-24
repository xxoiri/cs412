# mini_insta/admin.py
# register models for admin usage
# by Amy Ho, aho@bu.edu

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)

# add user to display
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'display_name', 'user']