from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'conditions', views.PatientConditionViewSet)
router.register(r'allergies', views.PatientAllergyViewSet)
router.register(r'reports', views.PatientReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
