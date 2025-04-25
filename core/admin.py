from django.contrib import admin
from .models import Exercise, Muscle, Profile, WorkoutSession, WorkoutLogging, FitnessGoal, PersonalRecord, Notification


# Register your models here.

admin.site.register(Exercise)
# admin.site.register(ExerciseCategory)
# admin.site.register(MuscleGroup)
admin.site.register(Muscle)
# admin.site.register(Equipment)
admin.site.register(Profile)
admin.site.register(WorkoutSession)
admin.site.register(WorkoutLogging)
admin.site.register(FitnessGoal)
admin.site.register(PersonalRecord)
admin.site.register(Notification)
