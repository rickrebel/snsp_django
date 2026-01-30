from category.models import (
    StatusControl, PriorityGroup, PlaceType, Topic, AgentType)
from api.views.common_views import BaseGenericViewSet


class StatusControlViewSet(BaseGenericViewSet):

    queryset = StatusControl.objects.all()


class PriorityGroupViewSet(BaseGenericViewSet):

    queryset = PriorityGroup.objects.all()


class PlaceTypeViewSet(BaseGenericViewSet):

    queryset = PlaceType.objects.all()


class TopicViewSet(BaseGenericViewSet):

    queryset = Topic.objects.all()


class AgentTypeViewSet(BaseGenericViewSet):

    queryset = AgentType.objects.all()
