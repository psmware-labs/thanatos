"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_header = "THANATOS Admin Portal"
admin.site.site_title = "Thanatos Admin"
admin.site.index_title = "Welcome to the Thanatos Admin Portal"

schema_view = get_schema_view(
    openapi.Info(
        title="Thanatos RESTful API Documentation",
        default_version='v1',
        description="Documentation of the Thanatos REST API, for consumption \
            of project Codename: Thanatos",
        terms_of_service="https://opensource.org/licenses/BSD-3-Clause",
        contact=openapi.Contact(email="pmclean@vso-inc.com"),
        license=openapi.License(name="AGPL3-only License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    path('api/user/', include('user.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/metrics/', include('metrics.urls')),
    path('api/questions/', include('questions.urls')),
]
