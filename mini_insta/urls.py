# mini_insta/urls.py
# by Amy Ho, aho@bu.edu

from django.urls import path
from .views import * # ProfileListView, ProfileView, PostDetailView, CreatePostView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
]