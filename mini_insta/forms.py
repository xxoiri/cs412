# mini_insta/forms.py
# form to create a post

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''class to create a form in order to create a new post on a profile.'''

    # data attributes
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

