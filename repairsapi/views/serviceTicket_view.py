from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket


class ServiceTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTicket
        fields = (
            "id",
            "description",
            "emergency",
            "date_completed",
            "employee",
            "customer",
        )
        depth = 1


class ServiceTicketView(ViewSet):
    def list(self, request):
        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()
        else:
            service_tickets = ServiceTicket.objects.filter(
                customer__user=request.auth.user
            )
        serialized = ServiceTicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        serviceTicket = ServiceTicket.objects.get(pk=pk)
        serialized = ServiceTicketSerializer(
            serviceTicket, context={"request": request}
        )
        return Response(serialized.data, status=status.HTTP_200_OK)