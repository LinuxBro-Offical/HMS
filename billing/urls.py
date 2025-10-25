from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'charge-types', views.ChargeTypeViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'refunds', views.RefundViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
