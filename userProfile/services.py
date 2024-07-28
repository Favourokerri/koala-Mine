import random
from .models import Profile
from authentication import services as authServices
from . import selectors

def createUserProfile(user):
    userProfile = Profile.objects.create(user=user)
    authServices.setVerificationCode(userProfile)
    return userProfile