from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import now, localtime

import random
import time
from datetime import datetime, timedelta

# list of images
imgs= ['https://media.discordapp.net/attachments/1185047338293678160/1411154768713486448/D76EA918-9BAC-4185-A91F-A1DB42B2CFBD.jpg?ex=68cab20a&is=68c9608a&hm=231ca3b9a0e037bac98633a367a1cd8e6c1de8aa3e9bb1b7e4ae9daf4944ac47&=&format=webp&width=1120&height=1992', 
       ]

# list of daily specials
specials=['Pho - $13.99', 'Bun Mam - $14.99',
          'Canh Bun - $12.99', 'Dan Dan Noodles - $11.99',
          'Hu Tieu - $12.99',]

# list of menu items
menu_items=[
    '23 Layer Chocolate Cake - $19.99',
    'Honey Glazed Ribs - $15.99',
    'Scallion Pancakes - $8.99',
    'Lychee Mocktail - $5.99',
    'Small Matcha Latte - $4.99',
    'Medium Matcha Latte - $5.99',
    'Large Matcha Latte - $6.99',
]

# Create your views here.
def main(request):
    ''' Respond to "main" request. '''
    template_name='restaurant/main.html'
    
    return render(request, template_name)

def order(request):
    ''' Respond to "order" request. '''
    template_name='restaurant/order.html'
    context= {
        "specials": random.choice(specials),
        "menu_items": menu_items,
    }

    return render(request, template_name, context)

def confirmation(request):
    ''' Process the order submission, generate a confirmation page and give an ETA. '''

    template_name = 'restaurant/confirmation.html'
    print(request.POST) 

    # check if POST data was sent with HTTP POST msg
    if request.POST:

        # extract form fields into variables
        # customer info
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_instructions = request.POST['special_instructions']

        # menu items and prices
        menu_items = {
            '23 Layer Chocolate Cake - $19.99': {'name': '23 Layer Chocolate Cake', 'price': 19.99},
            'Honey Glazed Ribs - $15.99': {'name': 'Honey Glazed Ribs', 'price': 15.99},
            'Lychee Mocktail - $5.99': {'name': 'Lychee Mocktail', 'price': 5.99},
            'Small Matcha Latte - $4.99': {'name': 'Small Matcha Latte', 'price': 4.99},
            'Medium Matcha Latte - $5.99': {'name': 'Medium Matcha Latte', 'price': 5.99},
            'Large Matcha Latte - 6.99': {'name': 'Large Matcha Latte', 'price': 6.99},
            'Scallion Pancakes - $8.99': {'name': 'Scallion Pancakes', 'price': 8.99},
            'Pho - $13.99': {'name': 'Pho', 'price': 13.99},
            'Bun Mam - $14.99': {'name': 'Bun Mam', 'price': 14.99},
            'Canh Bun - $12.99': {'name': 'Canh Bun', 'price': 12.99},
            'Dan Dan Noodles - $11.99': {'name': 'Dan Dan Noodles', 'price': 11.99},
            'Hu Tieu - $12.99': {'name': 'Hu Tieu', 'price': 12.99},
        }

        # get items ordered
        ordered_items = []
        total_price = 0.0

        # total price calculation
        for item_key in menu_items.keys():
            if item_key in request.POST:
                item = menu_items[item_key]
                ordered_items.append(f"{item['name']} - ${item['price']:.2f}")
                total_price += item['price']

        # generate random ETA 
        curr_time = now()
        eta_minutes = random.randint(30, 60) 
        ready_time = curr_time + timedelta(minutes=eta_minutes) - timedelta(hours=4)
        ready_time_str = localtime(ready_time).strftime('%I:%M %p')

        # create context vars for use in template
        context= {
            'ordered_items': ordered_items,
            'total_price': f"{total_price:.2f}",
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'readytime': ready_time_str,

        }
        return render(request, template_name=template_name, context=context)
    else:
        # default behavior
        template_name = 'restaurant/order.html'
        return render(request, template_name=order.html, context=context)
