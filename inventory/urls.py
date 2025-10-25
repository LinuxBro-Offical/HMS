from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'medicines', views.MedicineViewSet)
router.register(r'inventory', views.InventoryItemViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'stock-alerts', views.StockAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
