from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tests', views.LabTestViewSet)
router.register(r'orders', views.LabOrderViewSet)
router.register(r'results', views.LabResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
