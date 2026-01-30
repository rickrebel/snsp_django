from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from category.models import StatusControl

from ps_schema.models import Level, Collection, FilterGroup
from api.views.catalogs.serializers import (
    StatusControlSerializer,
    LevelSerializer,
    CollectionSerializer,
    FilterGroupSerializer,
)

class CatalogsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):

        catalogs = {
            # "user": UserProfileSerializer(
            #     User.objects.all(), many=True).data,

            "status_control": StatusControlSerializer(
                StatusControl.objects.all(), many=True).data,
            "levels": LevelSerializer(
                Level.objects.all(), many=True).data,
            "collections": CollectionSerializer(
                Collection.objects.all(), many=True).data,
            "filter_groups": FilterGroupSerializer(
                FilterGroup.objects.all(), many=True).data,

        }
        if not self.request.user.is_authenticated:
            catalogs["institution"] = []

        return Response(catalogs)
