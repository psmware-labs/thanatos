from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Account
from accounts import serializers


class BaseMetricAttributeViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin):
    """Base viewset to get IRT Accounts"""
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.order_by('name')

    def perform_create(self, serializer):
        """Create a new Account Attribute"""
        serializer.save(user=self.request.user)


class AccountViewSet(BaseMetricAttributeViewSet):
    """Manage accounts in the database"""
    queryset = Account.objects.all()
    serializer_class = serializers.AccountSerializer
