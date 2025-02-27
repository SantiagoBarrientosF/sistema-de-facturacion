from rest_framework import serializers # Importa el módulo de serialización de Django REST Framework
from sistema_facturacion.models import Invoice  # Importa el modelo Customers desde la aplicación

class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Invoice.
    Convierte instancias del modelo a formatos como JSON y viceversa.
    """
    class Meta:
        model = Invoice # Especifica el modelo al que pertenece el serializador
        fields = '__all__' # Incluye todos los campos del modelo en la serialización

    
