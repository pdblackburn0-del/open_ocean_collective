from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField

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


class Story(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    author_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')
    content = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.story.title}"


class TripSignup(models.Model):
    """Track user signups for surf trips"""
    TRIP_CHOICES = [
        ('cornwall-jan', 'Cornwall - January'),
        ('devon-feb', 'Devon - February'),
        ('pembrokeshire-mar', 'Pembrokeshire - March'),
        ('croyde-apr', 'Croyde - April'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_signups')
    trip = models.CharField(max_length=50, choices=TRIP_CHOICES)
    signed_up_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'trip')
        ordering = ['-signed_up_at']
    
    def __str__(self):
        return f"{self.user.username} signed up for {self.get_trip_display()}"


# Automatically create Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()