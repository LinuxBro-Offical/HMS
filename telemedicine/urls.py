from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sessions', views.TelemedicineSessionViewSet)
router.register(r'prescriptions', views.TelemedicinePrescriptionViewSet)
router.register(r'follow-ups', views.TelemedicineFollowUpViewSet)
router.register(r'devices', views.TelemedicineDeviceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
