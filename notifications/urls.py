from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'settings', views.TenantNotificationSettingViewSet)
router.register(r'templates', views.NotificationTemplateViewSet)
router.register(r'events', views.NotificationEventViewSet)
router.register(r'logs', views.NotificationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
