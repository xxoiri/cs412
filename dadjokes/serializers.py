# dadjokes/serializers.py
# Amy Ho, aho@bu.edu

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''
    A serializer for the Joke model.
    Specify which model/fields to send in the API.
    '''
    
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'created_at']
    
    def create(self, validated_data):
        '''
        Override the superclass method that handles object creation.
        '''
        print(f'JokeSerializer.create, validated_data={validated_data}.')
        
        # do the create and save all at once
        return Joke.objects.create(**validated_data)

class PictureSerializer(serializers.ModelSerializer):
    '''
    A serializer for the Picture model.
    Specify which model/fields to send in the API.
    '''
    
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created_at']