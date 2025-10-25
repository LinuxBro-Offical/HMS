from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'audit-logs', views.AuditLogViewSet)
router.register(r'privacy-consents', views.DataPrivacyConsentViewSet)
router.register(r'compliance-reports', views.ComplianceReportViewSet)
router.register(r'data-breach-incidents', views.DataBreachIncidentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
