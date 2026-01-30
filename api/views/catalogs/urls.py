from django.urls import include, path
from rest_framework import routers

from api.views.catalogs.all import CatalogsView
from api.views.category.views import (
    StatusControlViewSet, AgentTypeViewSet, PlaceTypeViewSet,
    PriorityGroupViewSet, TopicViewSet
)
from api.views.gob import ProgramViewSet, InstitutionViewSet
from api.views.user import RoleViewSet

router = routers.DefaultRouter()

# router.register(r'source', SourceViewSet, basename='catalog_source')
# router.register(r'status_control', StatusControlViewSet, basename='catalog_status_control')
# router.register(r'good_practice_package', GoodPracticePackageViewSet, basename='good_practice_package')
router.register(r'status_control', StatusControlViewSet, basename='catalog_status_control')
router.register(r'agent_type', AgentTypeViewSet, basename='catalog_agent_type')
router.register(r'place_type', PlaceTypeViewSet, basename='catalog_place_type')
router.register(r'priority_group', PriorityGroupViewSet, basename='catalog_priority_group')
router.register(r'topic', TopicViewSet, basename='catalog_topic')
router.register(r'program', ProgramViewSet, basename='catalog_program')
router.register(r'institution', InstitutionViewSet, basename='catalog_institution')
router.register(r'role', RoleViewSet, basename='catalog_role')


urlpatterns = [
    path("all/", CatalogsView.as_view(), name="catalogs_all"),
    path('', include(router.urls)),
]
