from rest_framework import serializers
from django.contrib import admin
from category.models import (
    StatusControl, PlaceType, Topic, PriorityGroup, 
    TopicGoal, AgentType
)


@admin.register(StatusControl)
class StatusControlAdmin(admin.ModelAdmin):
    list_display = [
        "public_name", "name", "group", "order",
        "color", "icon", "priority"]
    list_editable = ["order", "color", "icon", "priority"]
    list_filter = ["group"]


class PlaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceType
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class PriorityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityGroup
        fields = '__all__'


class TopicGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicGoal
        fields = '__all__'


class AgentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentType
        fields = '__all__'