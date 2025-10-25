from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'guidelines', views.ClinicalGuidelineViewSet)
router.register(r'drug-interactions', views.DrugInteractionViewSet)
router.register(r'alerts', views.ClinicalAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
