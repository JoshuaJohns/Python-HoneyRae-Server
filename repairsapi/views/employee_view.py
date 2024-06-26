from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "specialty", "full_name")


class EmployeeView(ViewSet):
    def list(self, request):
        employees = Employee.objects.all()
        serialized = EmployeeSerializer(employees, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        employee = Employee.objects.get(pk=pk)
        serialized = EmployeeSerializer(employee, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)
