from rest_framework import serializers
from .models import Profile
def getUserProfile(user):
    """ function to fetch profile by username"""
    try:
        return Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        raise serializers.ValidationError({"error": 'profile does not exit'})