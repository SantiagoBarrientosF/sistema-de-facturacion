from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from sistema_facturacion.models import Products
from sistema_facturacion.Serializers import ProductSerializer


@api_view(['GET', 'POST'])
 
def products_list(request):
    """
    Vista para listar todos los productos (GET) o crear un nuevo producto(POST).
    """
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def products_detail(request, dni):
    """
    Vista para obtener (GET), actualizar (PUT) o eliminar (DELETE) un producto específica.
    """
    products = get_object_or_404(Products, dni=dni)

    if request.method == 'GET':
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProductSerializer(products, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
