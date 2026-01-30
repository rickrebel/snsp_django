from rest_framework import viewsets, permissions

from api.pagination import CustomPagination
from rest_framework.response import Response
from geo.models import (
    State,
    Municipality,
    Locality,
    HealthDistrict)

from api.views.geo.serializers import (
    MunicipalityRetrieveSerializer,
    StateListSerializer,
    StateReportSerializer,
    MunicipalityListSerializer,
    LocalitySerializer,
    HealthDistrictSerializer,
    StateRetrieveSerializer,)


class ListSetMixin(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination


class StateListViewSet(ListSetMixin):
    queryset = State.objects.all().prefetch_related('municipalities')
    serializer_class = StateListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StateRetrieveSerializer
        return self.serializer_class


class StateReportViewSet(ListSetMixin):
    queryset = State.objects.all()
    serializer_class = StateReportSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StateRetrieveSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MunicipalityListViewSet(ListSetMixin):
    queryset = Municipality.objects.all().prefetch_related('localities')
    serializer_class = MunicipalityListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MunicipalityRetrieveSerializer
        return self.serializer_class


class LocalityListViewSet(ListSetMixin):
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer


class HealthDistrictListViewSet(ListSetMixin):
    queryset = HealthDistrict.objects.all()
    serializer_class = HealthDistrictSerializer

