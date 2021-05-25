from django.urls import path, include
from rest_framework.routers import DefaultRouter

from questions import views


router = DefaultRouter()
router.register('question', views.QuestionViewSet)

app_name = 'questions'

urlpatterns = [
    path('', include(router.urls))
]
