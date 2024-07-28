from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('signUp/', views.USerSignUpView.as_view(), name='signUp'),
    path('logIn/', views.LogInView.as_view(), name='logIn'),
    path('verifyEmail', views.VerifyEmail.as_view(), name='verifyEmail'),
    path('resendVerification', views.reSendVerification.as_view(), name='resendVerification')
]
