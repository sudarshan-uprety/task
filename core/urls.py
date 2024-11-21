"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from utils import env

schema_view = get_schema_view(
    openapi.Info(

        title="Khalti API",
        default_version='v1',
        description="This is for interview round.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="main@sudarshan-uprety.com.np"),
        license=openapi.License(name="Awesome License"),
    ),
    url=env.ROOT_URL,
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # swagger docs config
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # admin API
    path('admin/', admin.site.urls),

    # api for each apps.
    path('api/v1/user/', include('apps.users.urls')),
    path('api/v1/events/', include('apps.events.urls')),
    path('api/v1/booking/', include('apps.booking.urls')),
    path('api/v1/tickets/', include('apps.tickets.urls')),

]
