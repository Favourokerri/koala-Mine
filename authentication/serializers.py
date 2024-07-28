from rest_framework import serializers
from . import services

class userSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        confirm_password = self.context.get('confirm_password')
        validated_data = services.validateData(data, confirm_password)
        return validated_data
        
    def create(self, validated_data):
        """ creation serializers"""
        user = services.createUser(validated_data)
        return user