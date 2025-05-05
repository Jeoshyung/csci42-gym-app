from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, FitnessGoalForm, ProfileSetupForm
from datetime import datetime

from .models import WorkoutSession, WorkoutLogging, Exercise, FitnessGoal, PersonalRecord, Notification, Muscle, Profile

from django.utils.timezone import now, timedelta
from django.db.models import Sum, Q
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count

import pytz

from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site


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
                profile = user.profile
                if not profile.weight or not profile.height or not profile.birthdate:
                    messages.info(
                        request, "Please complete your profile setup.")
                    return redirect('profilesetup')
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
            Profile.objects.create(user=user)
            messages.success(
                request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def index_view(request):
    user = request.user
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    today = now().astimezone(shanghai_tz).date()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    weekly_sessions = WorkoutSession.objects.filter(
        user=user,
        date__date__gte=start_of_week,
        date__date__lte=end_of_week
    )

    activity_per_day = [0] * 7
    for session in weekly_sessions:
        session_date = session.date.astimezone(shanghai_tz)
        weekday = session_date.weekday()
        activity_per_day[weekday] += 1

    week_labels = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        week_labels.append(day.strftime('%a'))

    goals = FitnessGoal.objects.filter(user=user)
    serialized_goals = json.dumps([
        {
            "name": goal.name,
            "current_value": 0,
            "target_value": goal.target_value,
            "unit": goal.unit,
            "period": goal.period
        }
        for goal in goals
    ])

    context = {
        "total_workouts": weekly_sessions.count(),
        "total_sets": WorkoutLogging.objects.filter(session__in=weekly_sessions).aggregate(total=Sum('sets'))['total'] or 0,
        "total_reps": WorkoutLogging.objects.filter(session__in=weekly_sessions).aggregate(total=Sum('reps'))['total'] or 0,
        "goals": goals,
        "serialized_goals": mark_safe(serialized_goals),
        "serialized_weekly_activity": mark_safe(json.dumps({
            'data': activity_per_day,
            'labels': week_labels
        })),
        "today_date": today.strftime("%B %d, %Y"),
    }
    return render(request, "index.html", context)


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        data = json.loads(request.body)
        if 'weight_unit' in data:
            target_unit = data['weight_unit']
            if target_unit in ['kg', 'lbs'] and target_unit != profile.weight_unit:
                profile.weight = profile.convert_weight(target_unit)
                profile.weight_unit = target_unit
        if 'height_unit' in data:
            target_unit = data['height_unit']
            if target_unit in ['cm', 'ft'] and target_unit != profile.height_unit:
                profile.height = profile.convert_height(target_unit)
                profile.height_unit = target_unit
        profile.save()
        return JsonResponse({'success': True})

    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


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
    # Get filter parameters
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'name')
    selected_levels = request.GET.getlist('level')
    selected_equipment = request.GET.getlist('equipment')
    selected_muscle_ids = request.GET.getlist('muscle')
    
    # Initialize base queryset
    exercises = Exercise.objects.all()
    
    # Apply filters
    if query:
        exercises = exercises.filter(name__icontains=query)
    
    if selected_levels:
        exercises = exercises.filter(level__in=selected_levels)
    
    if selected_equipment:
        exercises = exercises.filter(equipment__in=selected_equipment)
    
    if selected_muscle_ids:
        exercises = exercises.filter(primary_muscles__id__in=selected_muscle_ids)
    
    # Apply sorting
    exercises = exercises.order_by(sort_by)

    # Get all muscles and selected muscle objects
    all_muscles = Muscle.objects.all().order_by('name')
    selected_muscles = Muscle.objects.filter(id__in=selected_muscle_ids)

    # Pagination
    paginator = Paginator(exercises, 9)
    page_number = request.GET.get('page')
    exercises = paginator.get_page(page_number)
    
    # Prepare context
    context = {
        'exercises': exercises,
        'query': query,
        'sort_by': sort_by,
        'selected_levels': selected_levels,
        'selected_equipment': selected_equipment,
        'selected_muscles': selected_muscles,
        'selected_muscle_ids': selected_muscle_ids,  # Add this for checkbox persistence
        'all_muscles': all_muscles,
        'level_choices': Exercise.LEVEL_CHOICES,
        'equipment_choices': Exercise.EQUIPMENT_CHOICES,
        'category_choices': Exercise.CATEGORY_CHOICES,
    }
    
    return render(request, 'workouts.html', context)


@login_required
def add_goal_view(request):
    if request.method == 'POST':
        form = FitnessGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Goal added successfully!")
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

            personal_record, created = PersonalRecord.objects.get_or_create(
                user=request.user,
                exercise=exercise,
                defaults={
                    'weight': weight,
                    'unit': unit,
                    'reps': reps
                }
            )

            if not created:
                if float(weight) > personal_record.weight or int(reps) > personal_record.reps:
                    personal_record.weight = weight
                    personal_record.unit = unit
                    personal_record.reps = reps
                    personal_record.save()
                    messages.success(request, "Personal record updated successfully!")
                else:
                    messages.info(request, "No update made. The new record is not better than the existing one.")
            else:
                messages.success(request, "Personal record added successfully!")

            Notification.objects.create(
                user=request.user,
                title="New Personal Record!" if created else "Personal Record Updated!",
                message=f"Congratulations! You've set a new personal record for {exercise.name}: {weight}{unit} x {reps} reps",
                notification_type='personal_record',
                related_record=personal_record
            )

            return redirect('profile')

    exercises = Exercise.objects.all()
    return render(request, 'add_personal_record.html', {'exercises': exercises})


@login_required
def delete_personal_record_view(request, record_id):
    personal_record = get_object_or_404(
        PersonalRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        personal_record.delete()
        messages.success(request, "Personal record deleted successfully!")
        return redirect('profile')

    return render(request, 'delete_personal_record.html', {'personal_record': personal_record})


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()

    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = get_object_or_404(
                Notification, id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return redirect('notifications')

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
def profile_setup_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            profile.age = profile.calculate_age()
            profile.save()
            messages.success(request, "Profile setup completed successfully!")
            return redirect('index')
    else:
        form = ProfileSetupForm(instance=profile)
    return render(request, 'profile_setup.html', {'form': form})


@login_required
def update_weight(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        if weight:
            profile = request.user.profile
            profile.weight = weight
            profile.save()
            messages.success(request, "Weight updated successfully!")
        else:
            messages.error(request, "Invalid weight value.")
    return redirect('profile')


@login_required
def update_height(request):
    if request.method == 'POST':
        height = request.POST.get('height')
        if height:
            profile = request.user.profile
            profile.height = height
            profile.save()
            messages.success(request, "Height updated successfully!")
        else:
            messages.error(request, "Invalid height value.")
    return redirect('profile')


def password_reset_view(request):
     if request.method == 'POST':
         form = PasswordResetForm(request.POST)
         if form.is_valid():
             email = form.cleaned_data['email']
             users = form.get_users(email)
             if users:
                 for user in users:
                     current_site = get_current_site(request)
                     subject = 'Password Reset Request'
                     email_template_name = 'password_reset_email.html'
                     context = {
                         'email': email,
                         'domain': current_site.domain,
                         'site_name': current_site.name,
                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                         'user': user,
                         'token': default_token_generator.make_token(user),
                         'protocol': 'https' if request.is_secure() else 'http',
                     }
                     email_message = render_to_string(email_template_name, context)
                     send_mail(subject, email_message, None, [email])
                 messages.success(request, 'Password reset instructions have been sent to your email.')
                 return redirect('login')
             else:
                 messages.error(request, 'No user is associated with this email address.')
     else:
         form = PasswordResetForm()
 
     return render(request, 'password_reset.html', {'form': form})
