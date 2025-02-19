from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from sistema_facturacion.models import Customers
from sistema_facturacion.Serializers import CustomerSerializer

# Crear y Listar clientes
@api_view(['GET', 'POST'])
def customer_list(request):
    if request.method == 'GET':
        customers = Customers.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener, Actualizar y Eliminar un cliente
@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, dni):
    customer = get_object_or_404(Customers, dni=dni)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
