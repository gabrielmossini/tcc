from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    birthday = models.DateField(default="1950-01-01")

    """ ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')"""

    def __str__(self):
        return self.name
    
