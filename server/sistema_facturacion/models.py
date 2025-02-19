from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Customers(models.Model):
    dni = models.CharField(primary_key=True,null=False,max_length=200)
    name = models.CharField(null=False,max_length=200)
    lastname = models.CharField(null=False,max_length=200)
    email = models.EmailField(null=True)
    tel = models.CharField(null=True,max_length=200)   
    address = models.CharField(null=False,max_length=200)
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    def __str__(self):
        return f"{self.name} {self.lastname}"    

class Products(models.Model):
    cod = models.CharField(primary_key =True,max_length=200)
    product_name = models.CharField(blank=False,max_length=200)
    description = models.CharField(blank=False,max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    max_stock = models.PositiveIntegerField()
    min_stock = models.PositiveIntegerField()
    customer_dni = models.ForeignKey(Customers,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"this bought for {self.customer_dni.name} and the product's {self.product_name}"    
    

class Invoice(models.Model):  
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagada'),
        ('canceled', 'Cancelada'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
    ]

    invoice_id = models.AutoField(primary_key=True,null=False)
    customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=200,choices=STATUS_CHOICES,default="pending")
    total = models.DecimalField(max_digits=12,decimal_places=4,null=True)
    payment_method= models.CharField(max_length=200,choices=PAYMENT_METHOD_CHOICES)
    due_date = models.DateField(null=True,)
    
    class Meta:
        verbose_name  = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-date']
    def __str__(self):
        return f"{self.invoice_id} {self.customer}"    
    
    