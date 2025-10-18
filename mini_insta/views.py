# mini_insta/views.py
# views for the mini_insta application
# by Amy Ho, aho@bu.edu

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all Profiles.'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name= 'mini_insta/show_profile.html'
    context_object_name='profile'

class PostDetailView(DetailView):
    '''Display a single post.'''

    model = Post
    template_name='mini_insta/show_post.html'
    context_object_name='post'

class CreatePostView(CreateView):
    '''Display a form for post creation.'''

    template_name= 'mini_insta/create_post_form.html'
    model = Post
    fields = ['caption']

    def get_context_data(self, **kwargs):
        '''Add the profile object to the template context.'''
        context = super().get_context_data(**kwargs)
        # Get the profile from URL parameter
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(Profile, pk=profile_pk)
        context['profile'] = profile
        return context
    def form_valid(self, form):
        '''handles the form submission - create post and associated photo(s)'''
        
        # Get the profile from URL parameter
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(Profile, pk=profile_pk)

        # Set the profile for the post before saving
        post = form.save(commit=False)
        post.profile = profile
        post.save()

        # handle uploaded image files
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(
                post=post,
                image_file=file
            )

        # create the photo object with the image_url from the form 
        # image_url = self.request.POST.get('image_file')
        # if image_url:
        #     Photo.objects.create(
        #         post=post,
        #         image_url=image_url
        #     )

        # redirect to the newly created post's detail page
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to the newly created post's detail page.'''
        return reverse_lazy('show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(UpdateView):
    '''Display a form for handling the update a profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    '''View class to delete a post on a profile.'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after a successful delete.'''
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdatePostView(UpdateView):
    '''Display a form for handling the update to a post.'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after a successful update.'''
        return reverse_lazy('show_post', kwargs={'pk': self.object.pk})
    
class ShowFollowersDetailView(DetailView):
    '''View class to display followers for a profile.'''

    model = Profile
    template_name = 'mini_insta/show_followers.html'

class ShowFollowingDetailView(DetailView):
    '''View class to display following for a profile.'''

    model = Profile
    template_name = 'mini_insta/show_following.html'