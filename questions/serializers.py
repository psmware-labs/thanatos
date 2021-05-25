from rest_framework import serializers

from core.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question object"""

    class Meta:
        model = Question
        fields = ('id', 'primary_metric',
                  'secondary_metric', 'tertiary_metric')
        read_only_Fields = ('id',)
