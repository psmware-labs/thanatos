from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts import views

router = DefaultRouter()
router.register('accounts', views.AccountViewSet)

app_name = 'accounts'

urlpatterns = [
    path('', include(router.urls))
]
