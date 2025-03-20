from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=63)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.name} | {self.email}'

    def save(self, *args, **kwargs):
        if self.user.email != self.email:
            self.user.email = self.email
            self.user.save()
        super(Profile, self).save(*args, **kwargs)

class ExerciseCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class MuscleGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Muscle(models.Model):
    name = models.CharField(max_length=255)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, related_name="muscles")

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ExerciseCategory, on_delete=models.SET_NULL, null=True, related_name="exercises")
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.SET_NULL, null=True, related_name="exercises")
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, related_name="exercises")
    tutorial_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_sessions")
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d %H:%M')}"
    
class WorkoutLogging(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="entries")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"