from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=63)
    email = models.EmailField(max_length=254)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} | {self.email}'

    def save(self, *args, **kwargs):
        if self.user.email != self.email:
            self.user.email = self.email
            self.user.save()
        super(Profile, self).save(*args, **kwargs)

# class ExerciseCategory(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# class MuscleGroup(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# class Muscle(models.Model):
#     name = models.CharField(max_length=255)
#     muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, related_name="muscles")

#     def __str__(self):
#         return self.name

# class Equipment(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# class Exercise(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.ForeignKey(ExerciseCategory, on_delete=models.SET_NULL, null=True, related_name="exercises")
#     muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.SET_NULL, null=True, related_name="exercises")
#     equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, related_name="exercises")
#     tutorial_link = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.name


class Muscle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    FORCE_CHOICES = [
        ('static', 'Static'),
        ('pull', 'Pull'),
        ('push', 'Push'),
    ]
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    MECHANIC_CHOICES = [
        ('isolation', 'Isolation'),
        ('compound', 'Compound'),
    ]
    EQUIPMENT_CHOICES = [
        ('medicine ball', 'Medicine Ball'),
        ('dumbbell', 'Dumbbell'),
        ('body only', 'Body Only'),
        ('bands', 'Bands'),
        ('kettlebells', 'Kettlebells'),
        ('foam roll', 'Foam Roll'),
        ('cable', 'Cable'),
        ('machine', 'Machine'),
        ('barbell', 'Barbell'),
        ('exercise ball', 'Exercise Ball'),
        ('e-z curl bar', 'E-Z Curl Bar'),
        ('other', 'Other'),
    ]
    CATEGORY_CHOICES = [
        ('powerlifting', 'Powerlifting'),
        ('strength', 'Strength'),
        ('stretching', 'Stretching'),
        ('cardio', 'Cardio'),
        ('olympic weightlifting', 'Olympic Weightlifting'),
        ('strongman', 'Strongman'),
        ('plyometrics', 'Plyometrics'),
    ]

    name = models.CharField(max_length=255)
    force = models.CharField(
        max_length=10, choices=FORCE_CHOICES, blank=True, null=True)
    level = models.CharField(
        max_length=15, choices=LEVEL_CHOICES, default="beginner")
    mechanic = models.CharField(
        max_length=15, choices=MECHANIC_CHOICES, blank=True, null=True)
    equipment = models.CharField(
        max_length=50, choices=EQUIPMENT_CHOICES, blank=True, null=True)
    primary_muscles = models.ManyToManyField(
        Muscle, related_name='primary_exercises')
    secondary_muscles = models.ManyToManyField(
        Muscle, related_name='secondary_exercises', blank=True)
    instructions = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    images = models.JSONField(default=list)  # Store image paths as a list
    exercise_id = models.CharField(
        max_length=50, unique=True, default="temp_id")

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workout_sessions")
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d %H:%M')}"


class WorkoutLogging(models.Model):
    session = models.ForeignKey(
        WorkoutSession, on_delete=models.CASCADE, related_name="entries")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"


class FitnessGoal(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fitness_goals")
    name = models.CharField(max_length=255)  # e.g., "Workouts per week"
    target_value = models.FloatField()  # e.g., "3" workouts
    unit = models.CharField(max_length=50, blank=True,
                            null=True)  # e.g., "workouts"
    period = models.CharField(max_length=50, choices=[(
        'daily', 'Daily'), ('weekly', 'Weekly')], default='weekly')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.target_value} {self.unit} ({self.period})"


class PersonalRecord(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="personal_records")
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="personal_records")
    weight = models.FloatField()
    unit = models.CharField(max_length=50, blank=True, null=True)
    reps = models.PositiveIntegerField(default=1)
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exercise.name}: {self.weight}{self.unit} x {self.reps}"
