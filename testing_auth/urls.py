from testing_auth import views
from django.urls import path


urlpatterns = [
    path('password-strength/', views.verify_password_strength),
]
