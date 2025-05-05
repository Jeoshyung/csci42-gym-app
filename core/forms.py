from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import WorkoutSession, WorkoutLogging, Profile, FitnessGoal

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class WorkoutSessionForms(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['notes']

class WorkoutLoggingForm(forms.ModelForm):
    class Meta:
        model = WorkoutLogging
        fields = ['exercise', 'sets', 'reps']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email']

class FitnessGoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = ['name', 'target_value', 'unit', 'period']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Goal Name'}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target Value'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (e.g., workouts, grams)'}),
            'period': forms.Select(attrs={'class': 'form-control'}),
        }

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weight', 'weight_unit', 'height', 'height_unit', 'birthdate']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight'}),
            'weight_unit': forms.Select(attrs={'class': 'form-select'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height'}),
            'height_unit': forms.Select(attrs={'class': 'form-select'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }