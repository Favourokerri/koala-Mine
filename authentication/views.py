from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from . serializers import userSerializer
from . import services
from . import selectors
# Create your views here.

class USerSignUpView(APIView):
    def post(self, request):
        userData = request.data
        user_serializer = userSerializer(data=userData, context={
        'confirm_password': request.data.get('confirm_password')
        })
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogInView(APIView):
    def post(self, request):
        data = request.data
        if 'username' in data and 'password' in data:
            userToken = services.logInUser(data=data)
            if userToken:
                return Response({'token': userToken})
            else:
                return Response({'error': 'invalid credentials'})
        else:
            return Response({'error': 'username and/or password missing'});

class VerifyEmail(APIView):
    def post(self, request):
        data = request.data
        if 'email' in data and 'verificationCode' in data:
           user = selectors.getUserByUsername(data['email'])
           userProfile = services.verifyEmail(user, data['verificationCode'])
           if userProfile:
               return Response({'data': 'email verified successfully'})
        return Response({'error': 'email and/or password is required'})

class reSendVerification(APIView):
    def post(self, request):
        data = request.data
        if 'email' in data:
            services.reSendVerification(data['email'])
            return Response({'data': 'verification code has  been sent'})
        return Response({'error': 'email is required'})


