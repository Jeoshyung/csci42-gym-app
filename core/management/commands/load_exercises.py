import json
from django.core.management.base import BaseCommand
from core.models import Exercise, Muscle

class Command(BaseCommand):
    help = 'Load exercises from a JSON file'

    def handle(self, *args, **kwargs):
        with open('core/data/exercises.json', 'r') as file:
            data = json.load(file)

            for item in data:
                # Create or get primary muscles
                primary_muscles = []
                for muscle_name in item.get('primaryMuscles', []):
                    muscle, _ = Muscle.objects.get_or_create(name=muscle_name)
                    primary_muscles.append(muscle)

                # Create or get secondary muscles
                secondary_muscles = []
                for muscle_name in item.get('secondaryMuscles', []):
                    muscle, _ = Muscle.objects.get_or_create(name=muscle_name)
                    secondary_muscles.append(muscle)

                # Create the exercise
                img_prefix = 'https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/'
                exercise, created = Exercise.objects.get_or_create(
                    exercise_id=item['id'],
                    defaults={
                        'name': item['name'],
                        'force': item.get('force'),
                        'level': item.get('level'),
                        'mechanic': item.get('mechanic'),
                        'equipment': item.get('equipment'),
                        'instructions': '\n'.join(item.get('instructions', [])),
                        'category': item.get('category'),
                        'images': [img_prefix + image for image in item.get('images', [])],
                    }
                )

                # Add muscles to the exercise
                exercise.primary_muscles.set(primary_muscles)
                exercise.secondary_muscles.set(secondary_muscles)

        self.stdout.write(self.style.SUCCESS('Successfully loaded exercises'))