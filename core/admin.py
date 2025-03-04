from django.contrib import admin
from .models import Exercise, ExerciseCategory, MuscleGroup, Muscle, Equipment

# Register your models here.

admin.site.register(Exercise)
admin.site.register(ExerciseCategory)
admin.site.register(MuscleGroup)
admin.site.register(Muscle)
admin.site.register(Equipment)