from django.contrib import admin
from django.urls import path,include

from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve


schema_view = get_schema_view( 
        openapi.Info(
            title="Your API Title",
            default_version='v1',
            description="Your API description",
            terms_of_service="https://www.example.com/policies/terms/",
            contact=openapi.Contact(email="contact@example.com"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
 
    path('api/v1/information-gathering/',include('nmap.urls') ),
    path("api/v1/testing-auth/",include('testing_auth.urls') ),
    
    # for serving static files such as pdf
    path("api/v1/assets/<path:path>/", serve, {"document_root": settings.MEDIA_ROOT}),
    
]
 