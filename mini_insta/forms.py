# mini_insta/forms.py
# forms to edit models within the database.

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''a form to add a Post to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        
        model = Post
        # data attributes of the Post class
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''a form to handle an update to a Profile.'''
    
    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    '''a form to handle an update to a Post.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']