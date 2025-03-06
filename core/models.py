from django.db import models

# Create your models here.

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