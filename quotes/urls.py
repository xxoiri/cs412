# File: quotes/url.py

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specfic to the quotes app:
urlpatterns =[
    path(r'', views.home, name='home'),
    path(r'quote', views.quote, name='quote'),
    path(r'show_all', views.show_all, name='show_all'),
    path(r'about', views.about, name='about'),
]