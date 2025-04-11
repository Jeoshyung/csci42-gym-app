from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Exercise, Muscle, WorkoutSession, WorkoutLogging, FitnessGoal, PersonalRecord


class AuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='pass')
        self.profile = Profile.objects.create(
            user=self.user,
            name="Test User",
            email="testuser@example.com",
            weight=70.0,
            height=175.0,
            age=25
        )

        self.muscle1 = Muscle.objects.create(name="Biceps")
        self.muscle2 = Muscle.objects.create(name="Triceps")

        self.exercise = Exercise.objects.create(
            name="Bicep Curl",
            force="pull",
            level="beginner",
            mechanic="isolation",
            equipment="dumbbell",
            instructions="Curl the dumbbell upward.",
            category="strength",
            exercise_id="curl001"
        )
        self.exercise.primary_muscles.add(self.muscle1)
        self.exercise.secondary_muscles.add(self.muscle2)
        self.exercise.images = ["curl1.png", "curl2.png"]
        self.exercise.save()

        self.session = WorkoutSession.objects.create(user=self.user)
        self.workout_log = WorkoutLogging.objects.create(
            session=self.session,
            exercise=self.exercise,
            sets=3,
            reps=12
        )

        self.goal = FitnessGoal.objects.create(
            user=self.user,
            name="Weekly Workouts",
            target_value=3,
            unit="workouts",
            period="weekly"
        )

        self.record = PersonalRecord.objects.create(
            user=self.user,
            exercise=self.exercise,
            weight=20.0,
            unit="kg",
            reps=10
        )

    def test_profile_creation(self):
        self.assertEqual(str(self.profile), "Test User | testuser@example.com")
        self.assertEqual(self.profile.user.email, "testuser@example.com")

    def test_exercise_relationships(self):
        self.assertIn(self.muscle1, self.exercise.primary_muscles.all())
        self.assertIn(self.muscle2, self.exercise.secondary_muscles.all())

    def test_exercise_str(self):
        self.assertEqual(str(self.exercise), "Bicep Curl")

    def test_workout_session_str(self):
        self.assertIn(self.user.username, str(self.session))

    def test_workout_logging_str(self):
        self.assertEqual(str(self.workout_log), "Bicep Curl - 3x12")

    def test_fitness_goal_str(self):
        self.assertEqual(
            str(self.goal), "Weekly Workouts - 3 workouts (weekly)")

    def test_personal_record_str(self):
        self.assertEqual(str(self.record), "Bicep Curl: 20.0kg x 10")

    def test_images_stored_as_list(self):
        self.assertIsInstance(self.exercise.images, list)
        self.assertIn("curl1.png", self.exercise.images)
