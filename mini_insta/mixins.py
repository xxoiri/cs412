# mini_insta/mixins.py
# by Amy Ho, aho@bu.edu

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Profile

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    '''adds profile lookup for logged-in user'''
    
    def get_profile(self):
        '''get the profile associated with the logged-in user'''
        # For users with multiple profiles, get the first one
        profile = get_object_or_404(Profile, user=self.request.user)
        return profile
    
    def get_context_data(self, **kwargs):
        '''add profile to context'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['current_profile'] = self.get_profile()
            except:
                context['current_profile'] = None
        return context
    
    def get_login_url(self):
        return reverse_lazy('login')