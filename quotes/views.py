# file: quotes/views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random

# two lists. one of quotes, another of images
list_quotes= ["The man who says he can, and the man who says he can't are both correct.", "A great man is hard on himself; a small man is hard on others", "The gem can not be polished without friction, nor man perfected without trials."]
list_images= ["https://i.natgeofe.com/n/d7b042d8-ee0b-48a2-935c-5eddbbec0ed7/02-confucius.jpg", "https://images.chinahighlights.com/allpicture/2014/09/1641a5d991e84d21a23aa5ca_cut_600x550_241_1742308020.jpg", "https://taniamacedoreligionisu.weebly.com/uploads/7/8/2/2/78226348/318606103.jpg?306"]

# Create your views here.
def home(request):
    ''' Fund to respond to the "home" request. '''
    template_name = 'quotes/base.html'
    # dict of quotes and images
    context = {
        "quotes": random.choice(list_quotes),
        "images": random.choice(list_images),
    }
    return render(request, template_name, context)

def quote(request):
    ''' Fund to respond to the "quote" request. '''
    template_name = 'quotes/quote.html'
    # dict of quotes and images
    context = {
        "quotes": random.choice(list_quotes),
        "images": random.choice(list_images),
    }
    return render(request, template_name, context)

def show_all(request):
    ''' Fund to respond to the "show_all" request. '''
    template_name= 'quotes/show_all.html'
    context = {
        "quotes": list_quotes,
        "images": list_images
    }
    return render(request, template_name, context)

def about(request):
    ''' Fund to respond to the "about" request. '''
    template_name= 'quotes/about.html'
    
    return render(request, template_name)