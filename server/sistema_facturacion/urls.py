from django.urls import path
from sistema_facturacion.views.Customers import *
from sistema_facturacion.views.Invoice import *
from sistema_facturacion.views.Products import * 

urlpatterns = [
    path('customers/',customer_list, name= "customer-list"), 
    path('customers/<int:dni>/',customer_detail, name= "customer-detail"), 
    path('invoices/',invoice_list, name= "invoice-list"), 
    path('invoices/<int:invoice_id>/',invoice_detail, name= "invoice-detail"), 
    path('products/',products_list, name= "products-list"), 
    path('products/<str:cod>/',products_detail, name= "products-detail"), 
    path('invoices/download/<int:invoice_id>/', generate_invoice_pdf, name='generate-invoice-pdf'),
]