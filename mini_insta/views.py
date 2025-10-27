# mini_insta/views.py
# views for the mini_insta application
# by Amy Ho, aho@bu.edu

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from .mixins import ProfileLoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # If user is logged in, include their profile
        if self.request.user.is_authenticated:
            current_profile = self.request.user.profile_set.first()
        else:
            current_profile = None

        context['current_profile'] = current_profile
        return context

class PostDetailView(DetailView):
    '''Display a single post.'''

    model = Post
    template_name='mini_insta/show_post.html'
    context_object_name='post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        current_profile = self.request.user.profile_set.first() if self.request.user.is_authenticated else None

        # Determine if the current user has liked this post
        if current_profile:
            is_liked = Like.objects.filter(post=post, profile=current_profile).exists()
        else:
            is_liked = False

        # Add data to context
        context['current_profile'] = current_profile
        context['is_liked'] = is_liked
        return context

class CreatePostView(ProfileLoginRequiredMixin, CreateView):
    '''Display a form for post creation.'''

    template_name= 'mini_insta/create_post_form.html'
    model = Post
    fields = ['caption']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use the logged-in user's profile instead of URL parameter
        context['profile'] = self.get_profile()
        return context
    
    def form_valid(self, form):
        '''handles the form submission - create post and associated photo(s)'''
        
        # Get the profile of logged in user
        profile = self.get_profile()

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

        # redirect to the newly created post's detail page
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to the newly created post's detail page.'''
        return reverse_lazy('show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(ProfileLoginRequiredMixin, UpdateView):
    '''Display a form for handling the update a profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    def get_object(self):
        '''Get the profile for the logged in user.'''
        return self.get_profile()

class DeletePostView(ProfileLoginRequiredMixin, DeleteView):
    '''View class to delete a post on a profile.'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after a successful delete.'''
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdatePostView(ProfileLoginRequiredMixin, UpdateView):
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

class PostFeedListView(ProfileLoginRequiredMixin, ListView):
    '''View class to display list of posts.'''

    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        '''Get the post feed for the specific profile'''
        profile = self.get_profile()
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        '''Add the profile to context'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

class SearchView(ProfileLoginRequiredMixin, ListView):
    '''View class for searching Profiles and Posts.'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle GET requests and check for search query.'''
        if 'query' not in self.request.GET:
            # No query present, use logged-in user's profile
            profile = self.get_profile()
            return render(request, 'mini_insta/search.html', {
                'profile': profile
            })
        # Query present, continue with ListView processing
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Return Posts that match the search query.'''
        query = self.request.GET.get('query', '').strip()
        if query:
            return Post.objects.filter(
                Q(caption__icontains=query)
            ).order_by('-timestamp')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        '''Add search results and profile to context.'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '').strip()
        
        # Add profile object
        context['profile'] = self.get_profile()
        
        # Add query
        context['query'] = query
        
        # Add matching profiles
        if query:
            context['matching_profiles'] = Profile.objects.filter(
                Q(username__icontains=query) |
                Q(display_name__icontains=query) |
                Q(bio_text__icontains=query)
            )
        else:
            context['matching_profiles'] = Profile.objects.none()
        
        return context
    
class CreateProfileView(CreateView):
        '''View to create a new User and Profile. '''
        model = Profile
        form_class = CreateProfileForm
        template_name = 'mini_insta/create_profile_form.html'
        success_url = reverse_lazy('show_all_profiles')

        def get_context_data(self, **kwargs):
            '''Add UserCreationForm to the context.'''
            context = super().get_context_data(**kwargs)
            # Add the UserCreationForm to context
            context['user_form'] = UserCreationForm()
            return context

        def form_valid(self, form):
            '''Handle both User creation and Profile creation.'''
            # Reconstruct UserCreationForm from POST data
            user_form = UserCreationForm(self.request.POST)
            
            if user_form.is_valid():
                # Save the User and get the User object
                user = user_form.save()
                
                # Log the user in
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Attach the User to the Profile instance
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                
                return super().form_valid(form)
            else:
                # If UserCreationForm is invalid, re-render the form with errors
                return self.form_invalid(form)

        def form_invalid(self, form):
            '''Handle invalid form submission.'''
            # Re-create the context with UserCreationForm errors
            context = self.get_context_data()
            context['user_form'] = UserCreationForm(self.request.POST)
            return self.render_to_response(context)
        
class FollowView(ProfileLoginRequiredMixin, TemplateView):
    '''View to follow a profile.'''
    
    def dispatch(self, request, *args, **kwargs):
        # Get the profile to follow
        profile_to_follow = get_object_or_404(Profile, pk=self.kwargs['pk'])
        current_profile = self.get_profile()
        
        # Prevent self-following
        if profile_to_follow != current_profile:
            # Check if follow relationship already exists
            follow, created = Follow.objects.get_or_create(
                profile=profile_to_follow,
                follower_profile=current_profile
            )
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_follow.pk)
    
    

class DeleteFollowView(ProfileLoginRequiredMixin, TemplateView):
    '''View to unfollow a profile.'''

    def dispatch(self, request, *args, **kwargs):
        # Get the profile to unfollow
        profile_to_unfollow = get_object_or_404(Profile, pk=self.kwargs['pk'])
        current_profile = self.get_profile()
        
        # Delete the follow relationship if it exists
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=current_profile
        ).delete()
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_unfollow.pk)

class LikeView(ProfileLoginRequiredMixin, TemplateView):
    '''View to like a post.'''
    
    def dispatch(self, request, *args, **kwargs):
        # Get the post to like
        post_to_like = get_object_or_404(Post, pk=self.kwargs['pk'])
        current_profile = self.get_profile()
        
        # Prevent liking own post
        if post_to_like.profile != current_profile:
            # Check if like already exists
            like, created = Like.objects.get_or_create(
                post=post_to_like,
                profile=current_profile
            )
        
        # Redirect back to the post page
        return redirect('show_post', pk=post_to_like.pk)

class DeleteLikeView(ProfileLoginRequiredMixin, TemplateView):
    '''View to unlike a post.'''
    
    def dispatch(self, request, *args, **kwargs):
        # Get the post to unlike
        post_to_unlike = get_object_or_404(Post, pk=self.kwargs['pk'])
        current_profile = self.get_profile()
        
        # Delete the like relationship if it exists
        Like.objects.filter(
            post=post_to_unlike,
            profile=current_profile
        ).delete()
        
        # Redirect back to the post page
        return redirect('show_post', pk=post_to_unlike.pk)