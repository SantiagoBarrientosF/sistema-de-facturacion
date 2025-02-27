# Importa las herramientas necesarias de Django
from django.db import models
from django.utils import timezone  # Para manejar fechas y horas

# Modelo para representar a los clientes en el sistema
class Customers(models.Model):
    dni = models.CharField(primary_key=True, null=False, max_length=200)  # Identificación única del cliente
    name = models.CharField(null=False, max_length=200)  # Nombre del cliente
    lastname = models.CharField(null=False, max_length=200)  # Apellido del cliente
    email = models.EmailField(null=True)  # Email del cliente (opcional)
    tel = models.CharField(null=True, max_length=200)  # Teléfono del cliente (opcional)
    address = models.CharField(null=False, max_length=200)  # Dirección del cliente

    class Meta:
        verbose_name = "Customer"  # Nombre en singular en la interfaz de administración
        verbose_name_plural = "Customers"  # Nombre en plural en la interfaz de administración

    def __str__(self):
        """Devuelve una representación en cadena del cliente."""
        return f"{self.name} {self.lastname}"  


# Modelo para representar los productos en el sistema
class Products(models.Model):
    cod = models.CharField(primary_key=True, max_length=200)  # Código único del producto
    product_name = models.CharField(blank=False, max_length=200)  # Nombre del producto
    description = models.CharField(blank=False, max_length=200)  # Descripción del producto
    price = models.DecimalField(max_digits=12, decimal_places=4)  # Precio del producto con 4 decimales
    max_stock = models.PositiveIntegerField()  # Stock máximo permitido
    min_stock = models.PositiveIntegerField()  # Stock mínimo permitido
    customer_dni = models.ForeignKey(Customers, on_delete=models.CASCADE)  # Relación con un cliente (ForeignKey)

    class Meta:
        verbose_name = "Product"  # Nombre en singular en la interfaz de administración
        verbose_name_plural = "Products"  # Nombre en plural en la interfaz de administración

    def __str__(self):
        """Devuelve una representación en cadena del producto y el cliente que lo compró."""
        return f"Product: {self.product_name}, bought by {self.customer_dni.name}"  


# Modelo para representar las facturas en el sistema
class Invoice(models.Model):  
    # Opciones para el estado de la factura
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagada'),
        ('canceled', 'Cancelada'),
    ]

    # Opciones para el método de pago
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
    ]

    invoice_id = models.AutoField(primary_key=True, null=False)  # Identificador único de la factura
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)  # Relación con el cliente
    date = models.DateField(default=timezone.now)  # Fecha de emisión de la factura (por defecto, la fecha actual)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")  # Estado de la factura
    total = models.DecimalField(max_digits=12, decimal_places=4, null=True)  # Total de la factura
    payment_method = models.CharField(max_length=200, choices=PAYMENT_METHOD_CHOICES)  # Método de pago utilizado
    due_date = models.DateField(null=True)  # Fecha de vencimiento (opcional)

    class Meta:
        verbose_name = "Invoice"  # Nombre en singular en la interfaz de administración
        verbose_name_plural = "Invoices"  # Nombre en plural en la interfaz de administración
        ordering = ['-date']  # Ordena las facturas por fecha de emisión (descendente)

    def __str__(self):
        """Devuelve una representación en cadena de la factura."""
        return f"Invoice {self.invoice_id} - {self.customer}"  

    