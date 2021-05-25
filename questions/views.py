from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Question
from questions import serializers


class BaseMetricAttributeViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin):
    """Base viewset get question attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.order_by('primary_metric'). \
            order_by('secondary_metric').\
            order_by('tertiary_metric')

    def perform_create(self, serializer):
        """Create a new Question Attribute"""
        serializer.save(user=self.request.user)


class QuestionViewSet(BaseMetricAttributeViewSet):
    """Manage Question metrics in the database"""
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
