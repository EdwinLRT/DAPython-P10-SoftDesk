from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """User model"""
    age = models.PositiveIntegerField(blank=True, null=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
