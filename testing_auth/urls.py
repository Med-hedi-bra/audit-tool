from testing_auth import views
from django.urls import path


urlpatterns = [
    path('username-password-strength/', views.verify_username_and_password_strength),
]
