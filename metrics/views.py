from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import PrimaryMetric, SecondaryMetric, TertiaryMetric
from metrics import serializers


class BaseMetricAttributeViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin):
    """Base viewset to get bast metric attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-metric')

    def perform_create(self, serializer):
        """Create a new Metric Attribute"""
        serializer.save(user=self.request.user)


class PrimaryMetricViewSet(BaseMetricAttributeViewSet):
    """Manage primary metrics in the database"""
    queryset = PrimaryMetric.objects.all()
    serializer_class = serializers.PrimaryMetricSerializer


class SecondaryMetricViewSet(BaseMetricAttributeViewSet):
    """Manage Secondary metrics in the database"""
    queryset = SecondaryMetric.objects.all()
    serializer_class = serializers.SecondaryMetricSerializer


class TertiaryMetricViewSet(BaseMetricAttributeViewSet):
    """Manage Tertiary metrics in the database"""
    queryset = TertiaryMetric.objects.all()
    serializer_class = serializers.TertiaryMetricSerializer
