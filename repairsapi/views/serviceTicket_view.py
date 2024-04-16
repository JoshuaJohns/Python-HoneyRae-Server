from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Employee, Customer


class ServiceTicketEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "full_name", "specialty")


class ServiceTicketCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "full_name", "address")


class ServiceTicketSerializer(serializers.ModelSerializer):

    employee = ServiceTicketEmployeeSerializer(many=False)
    customer = ServiceTicketCustomerSerializer(many=False)

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
        service_tickets = []

        if request.auth.user.is_staff:

            service_tickets = ServiceTicket.objects.all()
            if "status" in request.query_params:
                if request.query_params["status"] == "done":
                    service_tickets = service_tickets.filter(
                        date_completed__isnull=False
                    )

                if request.query_params["status"] == "all":
                    pass

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

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        new_ticket = ServiceTicket()
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        new_ticket.description = request.data["description"]
        new_ticket.emergency = request.data["emergency"]
        new_ticket.save()

        serialized = ServiceTicketSerializer(new_ticket, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):

        ticket = ServiceTicket.objects.get(pk=pk)
        employee_id = request.data["employee"]
        assigned_employee = Employee.objects.get(pk=employee_id)
        ticket.employee = assigned_employee
        ticket.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk=None):
        serviceTicket = ServiceTicket.objects.get(pk=pk)
        serviceTicket.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
