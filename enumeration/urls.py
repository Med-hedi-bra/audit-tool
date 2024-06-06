from enumeration import views
from django.urls import path


urlpatterns = [
    path('username-password-strength/', views.verify_username_and_password_strength),
    path("check-role-authorization/", views.check_role_authorization),
    path("owasp-spider/",views.owasp_spider),
    path("owasp-ascan/", views.owasp_scan),
    path("owasp-report/<int:id>", views.get_owasp_report),

]
