from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLES = [
        ['ADMIN', 'Admin'],
        ['USER', 'User'],
        ['MANAGER', 'Manager']
    ]
    role = models.CharField(choices=ROLES, default='USER')


