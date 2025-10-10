# mini_insta/forms.py
# form to create a post

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''a form to add a Post to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        
        model = Post
        # data attributes of the Post class
        fields = ['caption']