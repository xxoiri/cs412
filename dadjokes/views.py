# dadjokes/view.py
# Amy Ho, aho@bu.edu

from django.shortcuts import render, get_object_or_404
from .models import *
import random

# Create your views here.
def home(request):
    '''Display one random joke and one random picture.'''
    template_name= 'dadjokes/base.html'
    
    all_jokes = list(Joke.objects.all())
    all_pictures = list(Picture.objects.all())

    context = {
        "joke": random.choice(all_jokes),
        "picture": random.choice(all_pictures),
    }

    return render(request, template_name, context)

def random_view(request):
    '''Display a random joke and random picture.'''
    template_name = 'dadjokes/random.html'

    all_jokes = list(Joke.objects.all())
    all_pictures = list(Picture.objects.all())

    context = {
        "joke": random.choice(all_jokes),
        "picture": random.choice(all_pictures),
    }

    return render(request, template_name, context)

def all_jokes(request):
    '''show all jokes'''
    template_name = 'dadjokes/show_all_jokes.html'

    all_jokes = list(Joke.objects.all())

    context = {
        "jokes": all_jokes,
    }

    return render(request, template_name, context)

def joke_detail(request, pk):
    ''' gets a specific joke's details. '''
    template_name = 'dadjokes/joke_detail.html'
    
    joke = get_object_or_404(Joke, pk=pk)
    
    context = {
        "joke": joke,
    }
    return render(request, template_name, context)


def all_pictures(request):
    '''show all pictures'''
    template_name = 'dadjokes/show_all_pictures.html'

    all_pictures = list(Picture.objects.all())

    context = {
        "pictures": all_pictures,
    }

    return render(request, template_name, context)

def picture_detail(request, pk):
    ''' gets a specific picture's detail. '''
    template_name = 'dadjokes/picture_detail.html'
    
    picture = get_object_or_404(Picture, pk=pk)
    
    context = {
        "picture": picture,
    }
    return render(request, template_name, context)

# imports for API Views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *

# API Views:
class JokeListAPIView(generics.ListCreateAPIView):
    '''
    An API view to return a listing of Jokes 
    and to create a Joke.
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

# Custom API views for random selection
from rest_framework.views import APIView
from rest_framework.response import Response

class RandomJokeAPIView(APIView):
    def get(self, request):
        jokes = list(Joke.objects.all())
        if jokes:
            random_joke = random.choice(jokes)
            serializer = JokeSerializer(random_joke)
            return Response(serializer.data)
        return Response({"detail": "No jokes available."})

class RandomPictureAPIView(APIView):
    def get(self, request):
        pictures = list(Picture.objects.all())
        if pictures:
            random_picture = random.choice(pictures)
            serializer = PictureSerializer(random_picture)
            return Response(serializer.data)
        return Response({"detail": "No pictures available."})