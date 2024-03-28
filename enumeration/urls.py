from enumeration import views
from django.urls import path


urlpatterns = [
    path('username-password-strength/', views.verify_username_and_password_strength),
    path("check-role-authorization/", views.check_role_authorization),

]
