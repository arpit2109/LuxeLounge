from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile/', views.get_user_profile, name='profile'),
    path('users/', views.get_all_users, name='all-users'),  # Add this line
]