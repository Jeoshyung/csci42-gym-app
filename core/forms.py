from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import WorkoutSession, WorkoutLogging, Profile

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