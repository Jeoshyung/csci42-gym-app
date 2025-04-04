import pandas as pd
from core.models import Exercise, ExerciseCategory, Muscle, MuscleGroup, Equipment
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Import exercise from csv"

    def handle(self, *args, **kwargs):
        file_path = "core/data/ExerciseListFinal.csv"
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            category, _ = ExerciseCategory.objects.get_or_create(name=row["category"])

            muscle_group, _ = MuscleGroup.objects.get_or_create(name=row["muscle_group"])

            muscle, _ = Muscle.objects.get_or_create(name=row["muscle"], muscle_group=muscle_group)

            equipment, _ = Equipment.objects.get_or_create(name=row["equipment"])

            tutorial_link = row["tutorial_link"] if pd.notna(row["tutorial_link"]) else None # For null tutorial link

            Exercise.objects.create(
                name=row["name"],
                description=row["description"] if pd.notna(row["description"]) else "No description",
                category=category, 
                muscle_group=muscle_group,  
                equipment=equipment,  
                tutorial_link=tutorial_link,
            )

        self.stdout.write(self.style.SUCCESS("Successfully imported exercises!"))