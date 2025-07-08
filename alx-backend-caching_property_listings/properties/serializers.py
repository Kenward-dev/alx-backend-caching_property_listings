from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer for the Property model.
    Converts model instances to JSON format and vice versa.
    """
    
    class Meta:
        model = Property
        fields = '__all__' 
        read_only_fields = ['created_at']  