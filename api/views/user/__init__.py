from api.views.common_views import BaseGenericViewSet
from user.models import Role


class RoleViewSet(BaseGenericViewSet):
    queryset = Role.objects.all()

