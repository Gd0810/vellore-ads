from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.verified else 'Not Verified'}"


class PasswordResetToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.username} - Token {self.token}"