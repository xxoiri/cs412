# dadjokes/urls.py
# Amy Ho, aho@bu.edu

# imports
from django.urls import path
from django.conf import settings
from . import views

# URL patterns
urlpatterns =[

    # regular
    path(r'', views.home, name='home'),
    path(r'random', views.random_view, name='random'),
    path(r'jokes', views.all_jokes, name='joke_list'),
    path(r'joke/<int:pk>', views.joke_detail, name='joke_detail'),
    path(r'pictures', views.all_pictures, name='picture_list'),
    path(r'picture/<int:pk>', views.picture_detail, name='picture_detail'),

    # for API
    path(r'api/', views.RandomJokeAPIView.as_view()),
    path(r'api/random/', views.RandomJokeAPIView.as_view()),
    path(r'api/jokes/', views.JokeListAPIView.as_view()),
    path(r'api/joke/<int:pk>/', views.JokeDetailAPIView.as_view()),
    path(r'api/pictures/', views.PictureListAPIView.as_view()),
    path(r'api/picture/<int:pk>/', views.PictureDetailAPIView.as_view()),
    path(r'api/random_picture/', views.RandomPictureAPIView.as_view()),

]