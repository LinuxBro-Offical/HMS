from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'external-systems', views.ExternalSystemViewSet)
router.register(r'sync-logs', views.DataSyncLogViewSet)
router.register(r'field-mappings', views.IntegrationMappingViewSet)
router.register(r'webhook-endpoints', views.WebhookEndpointViewSet)
router.register(r'integration-errors', views.IntegrationErrorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
