from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import health_check
from api.views.auth.login_views import UserLoginAPIView, CheckingViewSet

from api.views.ps_schemas.views import CollectionViewSet

router = DefaultRouter()

router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'validate_token', CheckingViewSet, basename='validate_token')


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('catalogs/', include('api.views.catalogs.urls')),
    path('geo/', include('api.views.geo.urls')),
    path('', include(router.urls)),
]
