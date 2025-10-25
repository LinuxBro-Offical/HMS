from rest_framework import serializers
from .models import Medicine, InventoryItem, PurchaseOrder, StockAlert


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class StockAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAlert
        fields = '__all__'