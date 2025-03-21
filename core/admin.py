from django.contrib import admin
from .models import Exercise, ExerciseCategory, MuscleGroup, Muscle, Equipment, Profile, WorkoutSession, WorkoutLogging, FitnessGoal


# Register your models here.

admin.site.register(Exercise)
admin.site.register(ExerciseCategory)
admin.site.register(MuscleGroup)
admin.site.register(Muscle)
admin.site.register(Equipment)
admin.site.register(Profile)
admin.site.register(WorkoutSession)
admin.site.register(WorkoutLogging)
admin.site.register(FitnessGoal)