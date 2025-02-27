from rest_framework import serializers  # Importa el módulo de serialización de Django REST Framework
from sistema_facturacion.models import Products  # Importa el modelo Products desde la aplicación

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Products.
    Convierte instancias del modelo a formatos como JSON y viceversa.
    """
    class Meta:
        model = Products # Especifica el modelo al que pertenece el serializador
        fields = '__all__' # Incluye todos los campos del modelo en la serialización
