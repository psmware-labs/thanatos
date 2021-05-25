
from rest_framework import serializers

from core.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account object"""

    class Meta:
        model = Account
        fields = ('id', 'name')
        read_only_Fields = ('id',)
