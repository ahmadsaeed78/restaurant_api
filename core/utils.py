from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO

def generate_pdf_bill(order):
    # Create a BytesIO buffer to save the PDF file in memory
    buffer = BytesIO()
    
    # Create a canvas for the PDF file
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set the title of the document
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, f"Bill for Order #{order.id}")
    
    # Order Information
    c.setFont("Helvetica", 12)
    c.drawString(30, 700, f"Customer Name: {order.customer_name}")
    c.drawString(30, 680, f"Menu Item: {order.menu_item.name}")
    c.drawString(30, 660, f"Quantity: {order.quantity}")
    c.drawString(30, 640, f"Price per Item: {order.menu_item.price} USD")
    
    # Total Price
    total_price = order.menu_item.price * order.quantity
    c.drawString(30, 620, f"Total Price: {total_price} USD")
    
    # Status of the Order
    c.drawString(30, 600, f"Status: {order.get_status_display()}")
    
    # Save the PDF to the buffer
    c.showPage()
    c.save()
    
    # Return the buffer content as a response (as a downloadable PDF file)
    buffer.seek(0)
    return buffer



# Example of a table-based layout for the bill
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_pdf_bill_v2(order):
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Define data for the table
    data = [
        ['Customer Name:', order.customer_name],
        ['Menu Item:', order.menu_item.name],
        ['Quantity:', str(order.quantity)],
        ['Price per Item:', f'{order.menu_item.price} USD'],
        ['Total Price:', f'{order.menu_item.price * order.quantity} USD'],
        ['Status:', order.get_status_display()],
    ]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    
    elements = [table]
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
