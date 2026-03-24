from rest_framework import serializers
from category.models import (
    PlaceType, Topic, PriorityGroup, AgentType
)


class PlaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceType
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class AgentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentType
        fields = '__all__'


class PriorityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityGroup
        fields = '__all__'

