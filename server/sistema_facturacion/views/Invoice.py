from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from sistema_facturacion.models import Invoice,Products
from sistema_facturacion.Serializers import InvoiceSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from decimal import Decimal

@api_view(['GET', 'POST'])
def invoice_list(request):
    if request.method == 'GET':
        customers = Invoice.objects.all()
        serializer = InvoiceSerializer(customers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)

    if request.method == 'GET':
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def generate_invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    customer = invoice.customer
    products = Products.objects.filter(customer_dni=customer)  
    print(products)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{invoice_id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle(f"Factura {invoice_id}")

    
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(200, 750, "Sale invoice")
    
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 730, f"Factura N°: {invoice.invoice_id}")
    pdf.drawString(50, 715, f"Fecha: {invoice.date}")
    pdf.drawString(50, 700, f"Cliente: {customer.name} {customer.lastname}")
    pdf.drawString(50, 685, f"Dirección: {customer.address}")
    pdf.drawString(50, 670, f"Teléfono: {customer.tel}")

    
    data = [["Code", "Description", "Quantity", "Unit value", "Total"]]
    for product in products:
        data.append([
            product.cod, 
            product.product_name, 
            1,  
            f"${product.price:.2f}", 
            f"${product.price:.2f}"
        ])
    
    table = Table(data, colWidths=[80, 200, 60, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(pdf, 50, 500)
    table.drawOn(pdf, 50, 600)

    # **Totales**
    pdf.drawString(400, 550, f"Subtotal: ${invoice.total:.2f}")
    pdf.drawString(400, 535, f"IVA (19%): ${(invoice.total * Decimal(0.19)):.2f}")
    pdf.drawString(400, 520, f"Total: ${(invoice.total * Decimal(1.19)):.2f}")

    pdf.save()
    return response
