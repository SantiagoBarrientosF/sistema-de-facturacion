from rest_framework import serializers  # Importa el módulo de serialización de Django REST Framework
from sistema_facturacion.models import Customers  # Importa el modelo Customers desde la aplicación

# Definición del serializador para el modelo Customers
class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Customers.
    Convierte instancias del modelo a formatos como JSON y viceversa.
    """

    class Meta:
        model = Customers  # Especifica el modelo al que pertenece el serializador
        fields = '__all__'  # Incluye todos los campos del modelo en la serialización
