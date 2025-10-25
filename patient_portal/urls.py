from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activities', views.PatientPortalActivityViewSet)
router.register(r'feedback', views.PatientFeedbackViewSet)
router.register(r'settings', views.PatientPortalSettingsViewSet)
router.register(r'health-goals', views.PatientHealthGoalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
