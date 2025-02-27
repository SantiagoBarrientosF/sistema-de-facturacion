from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from sistema_facturacion.models import Invoice, Products
from sistema_facturacion.Serializers import InvoiceSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from decimal import Decimal

@api_view(['GET', 'POST'])
def invoice_list(request):
    """
    Vista para listar todas las facturas (GET) o crear una nueva factura (POST).
    """
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def invoice_detail(request, invoice_id):
    """
    Vista para obtener (GET), actualizar (PUT) o eliminar (DELETE) una factura específica.
    """
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
    """
    Genera un archivo PDF con los detalles de la factura.

    Parámetros:
        - request: Petición HTTP
        - invoice_id: ID de la factura a generar en PDF

    Retorna:
        - Archivo PDF como respuesta HTTP para descarga.
    """

    # Obtiene la factura y los productos asociados al cliente de la factura
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    customer = invoice.customer
    products = Products.objects.filter(customer_dni=customer)  
    print(products)  # Solo para depuración, podrías eliminarlo en producción
    
    # Configura la respuesta HTTP para generar un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{invoice_id}.pdf"'

    # Creación del PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle(f"Factura {invoice_id}")

    # Encabezado de la factura
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(200, 750, "Sale Invoice")  # Título principal

    # Datos del cliente y de la factura
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 730, f"Factura N°: {invoice.invoice_id}")
    pdf.drawString(50, 715, f"Fecha: {invoice.date}")
    pdf.drawString(50, 700, f"Cliente: {customer.name} {customer.lastname}")
    pdf.drawString(50, 685, f"Dirección: {customer.address}")
    pdf.drawString(50, 670, f"Teléfono: {customer.tel}")

    # Tabla de productos con encabezados
    data = [["Código", "Descripción", "Cantidad", "Valor unitario", "Total"]]

    # Recorre los productos asociados a la factura y los agrega a la tabla
    for product in products:
        data.append([
            product.cod, 
            product.product_name, 
            1,  # Asumimos que la cantidad es siempre 1, esto podría mejorarse si hay una cantidad real
            f"${product.price:.2f}", 
            f"${product.price:.2f}"
        ])

    # Configuración de la tabla en el PDF
    table = Table(data, colWidths=[80, 200, 60, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),  # Encabezado en color gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto blanco en encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear todo al centro
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes en la tabla
    ]))

    # Ubicación de la tabla en la hoja
    table.wrapOn(pdf, 50, 500)
    table.drawOn(pdf, 50, 600)

    # Sección de totales
    pdf.drawString(400, 550, f"Subtotal: ${invoice.total:.2f}")
    pdf.drawString(400, 535, f"IVA (19%): ${(invoice.total * Decimal(0.19)):.2f}")
    pdf.drawString(400, 520, f"Total: ${(invoice.total * Decimal(1.19)):.2f}")

    # Guardar y devolver el PDF
    pdf.save()
    return response
