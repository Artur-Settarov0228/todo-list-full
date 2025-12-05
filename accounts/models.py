from django.db import models
from django.contrib.auth.models import AbstractUser  # Django standart User modelini kengaytirish uchun

# Create your models here.
class CustomUser(AbstractUser):
    # Django User modelini kengaytirib, role maydoni qo‘shamiz
    ROLES = [
        ['ADMIN', 'Admin'],       # Admin rolini belgilash
        ['USER', 'User'],         # Oddiy foydalanuvchi rolini belgilash
        ['MANAGER', 'Manager']    # Manager rolini belgilash
    ]
    role = models.CharField(choices=ROLES, default='USER')  
    # role maydoni: tanlovli (choices) va default qiymat 'USER'
