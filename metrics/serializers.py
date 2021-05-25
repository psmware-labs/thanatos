from rest_framework import serializers

from core.models import PrimaryMetric, SecondaryMetric, TertiaryMetric


class PrimaryMetricSerializer(serializers.ModelSerializer):
    """Serializer for Primary Metric object"""

    class Meta:
        model = PrimaryMetric
        fields = ('id', 'metric')
        read_only_Fields = ('id',)


class SecondaryMetricSerializer(serializers.ModelSerializer):
    """Serializer for Secondary Metric object"""

    class Meta:
        model = SecondaryMetric
        fields = ('id', 'metric')
        read_only_Fields = ('id',)


class TertiaryMetricSerializer(serializers.ModelSerializer):
    """Serializer for Tertiary Metric object"""

    class Meta:
        model = TertiaryMetric
        fields = ('id', 'metric')
        read_only_Fields = ('id',)
