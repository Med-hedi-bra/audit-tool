from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = (
    [
        path("ports-scan-domain", views.get_host_infomations_by_domain),
        path("ports-scan-ip", views.get_host_infomations_by_ip),
        path("scanner", views.get_all_port_scanner),
        path("scanner/<int:id>", views.get_port_scanner_by_id),
        path("dns-service", views.collect_ipv4_ipv6_mail_server),
        path("dns-service/ipv4", views.convert_domain_to_ipv4),
        path("dns-service/ipv6", views.convert_domain_to_ipv6),
        path("dns-service/mail-server", views.convert_domain_to_mail_server),
        path("get-report/<int:id>", views.get_repport),
        path('extract-robots-txt/', views.extract_robots_txt),
        path('get-technologies/', views.get_technologies),

    ]

)
