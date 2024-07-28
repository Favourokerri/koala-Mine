from django.contrib.auth.models import User
from rest_framework import serializers

def getUserByUsername(username):
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
       raise serializers.ValidationError({"error": 'user with this username does not exit'})

def getUserByEmail(email):
    try:
        user = User.objects.get(username=email)
        return user
    except User.DoesNotExist:
       raise serializers.ValidationError({"error": 'user with this email does not exit'})