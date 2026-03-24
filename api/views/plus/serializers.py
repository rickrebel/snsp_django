from rest_framework import serializers

from plus.models import TopicGoal


class TopicGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicGoal
        fields = '__all__'
