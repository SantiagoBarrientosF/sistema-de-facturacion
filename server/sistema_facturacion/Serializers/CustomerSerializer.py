from rest_framework import serializers
from sistema_facturacion.models import Customers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'  