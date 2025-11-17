# dadjokes/models.py
# Amy Ho, aho@bu.edu
from django.db import models

# Create your models here.
class Joke(models.Model):
    '''the joke submission by a user.'''
    # data attributes
    text = models.TextField()
    contributor = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    # str representation
    def __str__(self):
        return f'Joke submitted by {self.contributor} at {self.created_at}.'
    
class Picture(models.Model):
    '''a picture/gif'''
    # data attributes
    image_url = models.URLField()
    contributor = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    # str representation
    def __str__(self):
        return f'Picture submitted by {self.contributor}.'