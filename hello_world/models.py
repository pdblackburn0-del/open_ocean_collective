from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ABILITY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    surfing_ability = models.CharField(max_length=20, choices=ABILITY_CHOICES, blank=True)
    county = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"