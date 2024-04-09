"""View module for handling requests for customer data"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "user", "address")


class CustomerView(ViewSet):
    def list(self, request):
        customers = Customer.objects.all()
        serialized = CustomerSerializer(customers, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        customer = Customer.objects.get(pk=pk)
        serialized = CustomerSerializer(customer, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)
