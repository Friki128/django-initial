from .models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Author
        fields=['first_name', 'last_name', 'date_of_birth', 'date_of_death']
