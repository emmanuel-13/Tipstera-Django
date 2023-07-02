from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    PROFILE_TYPES = (
        ('bettor', 'BETTOR'),
        ('tipster', 'TIPSTER'),
    )
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPES, default='bettor')
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.get_full_name()
