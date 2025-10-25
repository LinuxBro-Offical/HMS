from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'encounters', views.EncounterViewSet)
router.register(r'prescriptions', views.PrescriptionViewSet)
router.register(r'prescription-items', views.PrescriptionItemViewSet)
router.register(r'reports', views.EncounterReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
