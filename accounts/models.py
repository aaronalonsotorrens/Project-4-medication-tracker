from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s profile"
    