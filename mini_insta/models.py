# mini_insta/models.py
# display all models for mini_insta app
# by Amy Ho, aho@bu.edu
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a profile of a user on insta.'''

    # define the data attributes of the Profile object
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
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
        '''returns URL corresponding to the profile that was updated.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_followers(self):
        '''returns list of follower profiles.'''
        followers = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in followers]
    
    def get_num_followers(self):
        '''returns the count of followers for this profile.'''
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        '''returns a list of Profiles that this profile is following.'''
        following = Follow.objects.filter(follower_profile = self)
        return [follow.profile for follow in following]
    
    def get_num_following(self):
        '''returns the count of how many profiles this profile is following.'''
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        '''shows post for each of the profiles being followed by a given user with 
        the most recent at the top.'''
        following_profiles = self.get_following()
        posts = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
        return posts
    
    def is_followed_by(self):
        '''check if this profile is followed by another profile'''
        return Follow.objects.filter(profile=self, follower_profile=profile).exists()
    
class Post(models.Model):
    '''Model the data attributes of an Instagram Post.'''

    # define the data attributes of the Post object
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='posts')
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.profile} created a post at {self.timestamp} captioned {self.caption}.'
    
    def get_all_photos(self):
        '''a getter method to find and return all Photos for a given Post.'''
        return Photo.objects.filter(post=self)
    
    def get_all_comments(self):
        '''find and return all comments for a post.'''
        return Comment.objects.filter(post=self)
    
    def get_likes(self):
        '''find and return all likes on a post.'''
        return Like.objects.filter(post=self)
    
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
        
class Follow(models.Model):

    '''encapsulates the idea of an edge connecting two nodes. 
        this relation will associate 2 profiles.'''
    
    # define the data attributes
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='followed_by')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''method to view Follow relationship as a string rep.'''
        return f'{self.follower_profile} follows {self.profile}.'
    
class Comment(models.Model):
    '''models a comment on a profile's post.'''

    # define the data attributes
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_comments')
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''allows viewing as str representation.'''
        return f'{self.profile} said {self.text} on the post: {self.post} at {self.timestamp}.'
    
class Like(models.Model):
    '''models the likes on a profile's post.'''

    # data attributes
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="liked_by")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns string rep of when this like was created'''
        return f'{self.profile} liked {self.post} at {self.timestamp}.'