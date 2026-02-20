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


class Meetup(models.Model):
    LOCATION_CHOICES = [
        ('bristol', 'The Wave (Bristol)'),
        ('cornwall', 'Newquay (Cornwall)'),
        ('wales', 'Pembrokeshire (Wales)'),
    ]

    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, unique=True)
    description = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meetup at {self.get_location_display()}"

    class Meta:
        ordering = ['location']


class MeetupSignup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetup_signups')
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE, related_name='signups')
    signed_up_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meetup')

    def __str__(self):
        return f"{self.user.username} signed up for {self.meetup.get_location_display()}"