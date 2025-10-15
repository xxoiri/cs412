# mini_insta/models.py
# display all models for mini_insta app
# by Amy Ho, aho@bu.edu
from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a profile of a user on insta.'''

    # define the data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.username} or 'f'{self.display_name}'
    
    def get_all_posts(self):
        '''a getter method to find and return all Posts for a given profile.'''
        return Post.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        '''a special method, returns URL corresponding to the profile that was updated.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
class Post(models.Model):
    '''Model the data attributes of an Instagram Post.'''

    # define the data attributes of the Post object
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='posts')
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.profile} created a post at 'f'{self.timestamp}'
    
    def get_all_photos(self):
        '''a getter method to find and return all Photos for a given Post.'''
        return Photo.objects.filter(post=self)
    
class Photo(models.Model):
    '''Model the data attributes of an image associated with a Post.'''

    # define the data attributes of the Photo object
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(blank=True) # image URL string
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True) # an image file

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.post} created at 'f'{self.timestamp}'

    def get_image_url(self):
        '''accessor method that will return the URL to the image.
            returns image_URL if it exists, else it returns image_file attribute.'''
        if self.image_file:
            return self.image_file.url
        else:
            return self.image_url
        
