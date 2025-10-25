from rest_framework import viewsets, permissions
from .models import ChargeType, Invoice, Payment, Refund
from .serializers import ChargeTypeSerializer, InvoiceSerializer, PaymentSerializer, RefundSerializer


class ChargeTypeViewSet(viewsets.ModelViewSet):
    queryset = ChargeType.objects.all()
    serializer_class = ChargeTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]