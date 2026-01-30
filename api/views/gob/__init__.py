from api.views.common_views import BaseGenericViewSet
from gob.models import Program, Institution


class ProgramViewSet(BaseGenericViewSet):
    queryset = Program.objects.all()


class InstitutionViewSet(BaseGenericViewSet):
    queryset = Institution.objects.all()
