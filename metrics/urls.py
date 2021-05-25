from django.urls import path, include
from rest_framework.routers import DefaultRouter

from metrics import views


router = DefaultRouter()
router.register('primarymetric', views.PrimaryMetricViewSet)
router.register('secondarymetric', views.SecondaryMetricViewSet)
router.register('tertiarymetric', views.TertiaryMetricViewSet)

app_name = 'metrics'

urlpatterns = [
    path('', include(router.urls))
]
