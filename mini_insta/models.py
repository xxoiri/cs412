from django.db import models

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