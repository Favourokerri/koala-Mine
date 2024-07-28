from django.contrib.auth.models import User
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import serializers
from userProfile.models import Profile
from . import selectors
from userProfile import services as profileServices
from userProfile import selectors as profileSelector
from django.core.mail import send_mail
from django.conf import settings

def validateData(data, confirm_password):
    """ function for validating data"""
    data['username'] = data['email']
        
    if data['password'] != confirm_password:
        raise serializers.ValidationError({"password": "Password and confirm password do not match."})
    if len(data['password']) < 8:
        raise serializers.ValidationError({"password": "Length must be greater than 8"})
    return data

def createUser(validated_data):
    """ function to create users"""
    try:
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.password = make_password(password)
        userProfile = profileServices.createUserProfile(user)
        send_verification_email(user.email, userProfile.verificationCode)
        user.save()
        return user

    except IntegrityError:
        raise serializers.ValidationError({"error": 'user with this username already exits'})

def setVerificationCode(userProfile):
    verification_code = ''.join(str(random.randint(0, 9)) for _ in range(4))
    userProfile.verificationCode =  verification_code
    userProfile.verificationCodeExpiresAt = timezone.now() + timedelta(minutes=5)
    userProfile.save()
    return verification_code

def send_verification_email(to_email, verification_code):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {verification_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list)

def reSendVerification(email):
    user = selectors.getUserByEmail(email)
    userProfile = profileSelector.getUserProfile(user)
    verificationCode = setVerificationCode(userProfile)
    send_verification_email(user.email, verificationCode)
    

def verifyEmail(user, verificationCode):
    """ function to verify user email"""
    userProfile = profileSelector.getUserProfile(user)
    is_Code_Correct = userProfile.verificationCode == verificationCode
    is_code_not_expired = userProfile.verificationCodeExpiresAt > timezone.now() 
    if is_Code_Correct and is_code_not_expired:
        userProfile.is_verified = True
        userProfile.save()
        return userProfile
    else:
         raise serializers.ValidationError({"unVerified": 'Invalid or expired verification code'})

def logInUser(data):
    """ function for user login"""
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user:
        userProfile = profileSelector.getUserProfile(user)
        if userProfile.is_verified:
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return token.key
        else:
            raise serializers.ValidationError({"unVerified": 'please verify your profile'})
    else:
        return None