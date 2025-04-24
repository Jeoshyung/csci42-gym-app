from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import LoginForm, RegisterForm, FitnessGoalForm
from datetime import datetime
from .models import WorkoutSession, WorkoutLogging, Exercise, FitnessGoal, PersonalRecord, Notification
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json

def exercise_detail_view(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = request.POST.get('remember_me')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(86400)
                else:
                    request.session.set_expiry(0)
                    request.session.modified = True

                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def index_view(request):
    user = request.user

    start_of_week = now().date() - timedelta(days=now().weekday()
                                             )  # Start of the current week
    weekly_sessions = WorkoutSession.objects.filter(
        user=user, date__date__gte=start_of_week)

    total_workouts = weekly_sessions.count()
    total_sets = sum(session.entries.aggregate(total_sets=Sum('sets'))[
                     'total_sets'] or 0 for session in weekly_sessions)
    total_reps = sum(session.entries.aggregate(total_reps=Sum('reps'))[
                     'total_reps'] or 0 for session in weekly_sessions)

    goals = FitnessGoal.objects.filter(user=user)

    # Add progress percentage for each goal
    for goal in goals:
        if goal.period == 'weekly':
            # SAMPLE LOGIC: For weekly goals, progress is the total number of workouts logged in the current week
            progress_value = total_workouts if goal.name.lower() == 'workout' else 0
            # Add more logic here for specific goals
        else:
            progress_value = 0  # Add logic for daily goals if needed
        goal.current_value = progress_value
        goal.progress_percentage = min(
            100, (progress_value / goal.target_value) * 100)
        goal.target_value = int(goal.target_value)  # for frontend display

    # Serialize goals for JavaScript; for progress bars
    serialized_goals = json.dumps(
        [{'name': goal.name, 'current_value': goal.current_value,
            'target_value': goal.target_value} for goal in goals],
        cls=DjangoJSONEncoder
    )

    context = {
        'today_date': datetime.today().strftime('%B %d, %Y'),
        'total_workouts': total_workouts,
        'total_sets': total_sets,
        'total_reps': total_reps,
        'goals': goals,
        'serialized_goals': mark_safe(serialized_goals),
    }
    return render(request, 'index.html', context)


@login_required
def profile_view(request):
    exercises = Exercise.objects.all()
    return render(request, 'profile.html', {'exercises': exercises})


@login_required
def workout_logger_view(request):
    past_sessions = WorkoutSession.objects.filter(
        user=request.user).order_by('-date')

    if request.method == 'POST':
        selected_exercise_id = request.POST.get('exercise')
        sets = request.POST.get('sets')
        reps = request.POST.get('reps')
        notes = request.POST.get('notes', '')

        if selected_exercise_id and sets and reps:
            exercise = Exercise.objects.get(id=selected_exercise_id)

            session, created = WorkoutSession.objects.get_or_create(
                user=request.user,
                date__date=datetime.today().date(),
                defaults={'notes': notes}
            )

            WorkoutLogging.objects.create(
                session=session, exercise=exercise, sets=sets, reps=reps
            )
            messages.success(request, "Workout logged successfully!")
            return redirect('workout_logger')

    exercises = Exercise.objects.all()
    return render(request, 'workoutsession.html', {
        'past_sessions': past_sessions,
        'exercises': exercises
    })


@login_required
def workouts_view(request):
    query = request.GET.get('q', '')
    if query:
        exercises_list = Exercise.objects.filter(name__icontains=query)
    else:
        exercises_list = Exercise.objects.all()

    paginator = Paginator(exercises_list, 9)

    page_number = request.GET.get('page')
    exercises = paginator.get_page(page_number)
    return render(request, 'workouts.html', {'exercises': exercises, 'query': query})


@login_required
def add_goal_view(request):
    if request.method == 'POST':
        form = FitnessGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user  # Associate the goal with the logged-in user
            goal.save()
            messages.success(request, "Goal added successfully!")
            # Redirect to the index page after adding the goal
            return redirect('index')
    else:
        form = FitnessGoalForm()

    return render(request, 'add_goal.html', {'form': form})


@login_required
def add_personal_record_view(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise')
        weight = request.POST.get('weight')
        unit = request.POST.get('unit')
        reps = request.POST.get('reps', 1)

        if exercise_id and weight and unit:
            exercise = get_object_or_404(Exercise, id=exercise_id)
            
            # Create the personal record
            personal_record = PersonalRecord.objects.create(
                user=request.user,
                exercise=exercise,
                weight=weight,
                unit=unit,
                reps=reps
            )

            # Create notification for the new personal record
            Notification.objects.create(
                user=request.user,
                title="New Personal Record!",
                message=f"Congratulations! You've set a new personal record for {exercise.name}: {weight}{unit} x {reps} reps",
                notification_type='personal_record',
                related_record=personal_record
            )

            messages.success(request, "Personal record added successfully!")
            return redirect('profile')

    exercises = Exercise.objects.all()
    return render(request, 'add_personal_record.html', {'exercises': exercises})


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return redirect('notifications')
    
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
