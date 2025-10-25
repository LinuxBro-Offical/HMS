from rest_framework import serializers
from .models import ExternalSystem, DataSyncLog, IntegrationMapping, WebhookEndpoint, IntegrationError

class ExternalSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSystem
        fields = '__all__'

class DataSyncLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSyncLog
        fields = '__all__'

class IntegrationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationMapping
        fields = '__all__'

class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = '__all__'

class IntegrationErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationError
        fields = '__all__'
