# mini_insta/urls.py

from django.urls import path
from .views import ProfileListView, ProfileView, PostDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
]