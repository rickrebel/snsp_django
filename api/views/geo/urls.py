from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.geo import (
    StateListViewSet,
    MunicipalityListViewSet,
    LocalityListViewSet,
    HealthDistrictListViewSet
)

router = DefaultRouter()

router.register(r'state', StateListViewSet, basename='geo_state')
router.register(
    r'municipality', MunicipalityListViewSet, basename='geo_municipality')
router.register(r'locality', LocalityListViewSet, basename='geo_locality')
router.register(
    r'health-district', HealthDistrictListViewSet,
    basename='geo_health_district'
)

urlpatterns = [
    path('', include(router.urls)),
]
