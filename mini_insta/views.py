# mini_insta/views.py
# views for the mini_insta application

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all Profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name= 'mini_insta/profile.html'
    context_object_name='profile' 

class RandomProfileView(DetailView):
    '''Display a single profile selected at random.'''