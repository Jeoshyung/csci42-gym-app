from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, register_view, index_view, profile_view, workouts_view, workout_logger_view, add_goal_view, add_personal_record_view, exercise_detail_view, notifications_view, profile_setup_view, update_weight, update_height, password_reset_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
     path('login/', login_view, name='login'),
     path('register/', register_view, name='register'),
     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
     path('', index_view, name='index'),
     path("profile/", profile_view, name="profile"),
     path('workoutlogging/', workout_logger_view, name='workout_logger'),
     # path('password-reset/', auth_views.PasswordResetView.as_view(),
     #      name='password_reset'),
     path('password-reset/', password_reset_view, name='password_reset'),
     path('workouts/', workouts_view, name='workouts'),
     path('add-goal/', add_goal_view, name='add_goal'),
     path("add-personal-record/", add_personal_record_view,
         name="add_personal_record"),
     path('exercise/<int:exercise_id>/', exercise_detail_view, name='exercise_detail'),
     path('notifications/', notifications_view, name='notifications'),
     path('profilesetup/', profile_setup_view, name='profilesetup'),
    path('update-weight/', update_weight, name='update_weight'),
    path('update-height/', update_height, name='update_height'),
]
