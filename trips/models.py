from django.db import models

# Create your models here.
from django.db import models
from users.models import User

class Trip(models.Model):
    CATEGORY_CHOICES = [
        ('AD', 'Adventure'),
        ('FD', 'Food'),
        ('ST', 'Sightseeing'),
        ('OT', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    group_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_trips')
    created_at = models.DateTimeField(auto_now_add=True)
    trip_code = models.CharField(max_length=8, unique=True)
    
    def __str__(self):
        return self.name

class TripParticipant(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('trip', 'user')
    
    def __str__(self):
        return f"{self.user.username} in {self.trip.name}"

class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('AD', 'Adventure'),
        ('FD', 'Food'),
        ('ST', 'Sightseeing'),
        ('OT', 'Other'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='OT')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class ActivityVote(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    vote = models.BooleanField(default=True)  # True for upvote, False for downvote
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('activity', 'user')
    
    def __str__(self):
        return f"{self.user.username} voted on {self.activity.title}"
    
