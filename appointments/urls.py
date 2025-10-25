from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'doctor-schedules', views.DoctorScheduleViewSet)
router.register(r'token-counters', views.TokenCounterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
