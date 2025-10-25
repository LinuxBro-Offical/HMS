from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patient-analytics', views.PatientAnalyticsViewSet)
router.register(r'clinic-analytics', views.ClinicAnalyticsViewSet)
router.register(r'doctor-performance', views.DoctorPerformanceViewSet)
router.register(r'revenue-analytics', views.RevenueAnalyticsViewSet)
router.register(r'custom-reports', views.CustomReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
