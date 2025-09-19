# File: restaurant/url.py

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specfic to the restaurant app:
urlpatterns =[
    path(r'', views.main, name='main'),
    path(r'main', views.main, name='main'),
    path(r'order', views.order, name='order'),
    path(r'confirmation', views.confirmation, name='confirmation'),
]