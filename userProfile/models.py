from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    """ models for userProfile"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verificationCode = models.CharField(max_length=6, editable=False)
    verificationCodeExpiresAt = models.DateTimeField(blank=True, null=True, editable=False)
    is_verified = models.BooleanField(default=False)