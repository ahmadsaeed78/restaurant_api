# views_multorder.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers_multorder import AggregateOrderSerializer

@api_view(['POST'])
def create_aggregate_order(request):
    """
    API endpoint to create a multi-item (aggregate) order.
    Expected payload:
    {
        "user": 1,  # optional, if registered
        "table": 1,  # optional
        "customer_name": "John Doe",
        "items": [
            {
                "menu_item": 5,
                "quantity": 2,
                "special_instructions": "Less spicy"
            },
            {
                "menu_item": 3,
                "quantity": 1,
                "special_instructions": ""
            }
        ]
    }
    """
    serializer = AggregateOrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        # If a table is specified, update its status to booked.
        if order.table:
            table = order.table
            table.is_booked = True
            table.save()
        return Response(AggregateOrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# views_multorder.py

from rest_framework import generics, permissions
from .models import AggregateOrder
from .serializers_multorder import AggregateOrderSerializer

# To list all aggregate orders (or filter by status, table, etc.)
class AggregateOrderListAPIView(generics.ListAPIView):
    queryset = AggregateOrder.objects.all().order_by('-created_at')
    serializer_class = AggregateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust as needed

# To retrieve a single aggregate order
class AggregateOrderRetrieveAPIView(generics.RetrieveAPIView):
    queryset = AggregateOrder.objects.all()
    serializer_class = AggregateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from .models import AggregateOrder, Table
from .serializers_multorder import AggregateOrderSerializer

@api_view(["PATCH"])
@permission_classes([IsAuthenticated]) 
def update_order_status(request, order_id):
    """
    Update the status of an order. If marked as 'Paid', also update the table's is_booked status to False.
    """
    order = get_object_or_404(AggregateOrder, id=order_id)
    new_status = request.data.get("status")

    if new_status not in ["Delivered", "Completed", "Paid"]:
        return Response({"error": "Invalid status update"}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()

    if new_status == "Paid":
        # Mark the table as unbooked
        if order.table:
            order.table.is_booked = False
            order.table.save()

    return Response({"message": "Order status updated", "order": AggregateOrderSerializer(order).data})


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from core.models import AggregateOrder, AggregateOrderItem
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from core.models import AggregateOrder, AggregateOrderItem

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_bill(request, order_id):
    try:
        order = AggregateOrder.objects.get(id=order_id)
        print(f"Order found: {order.id}, Total: {order.total_price}")
        
        items = AggregateOrderItem.objects.filter(order=order)
        print(f"Found {len(items)} items for this order.")

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="bill_{order_id}.pdf"'

        pdf = canvas.Canvas(response)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 800, "Restaurant Bill")
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 770, f"Order ID: {order.id}")
        pdf.drawString(100, 750, f"Total Price: Rs.{order.total_price}")
        pdf.drawString(100, 730, "Items Ordered:")

        y_position = 710
        for item in items:
            print(f"Adding item to bill: {item.menu_item.name} x {item.quantity}")  # Debug print
            pdf.drawString(120, y_position, f"- {item.menu_item.name} x {item.quantity}")
            y_position -= 20  # Move down for next item

        pdf.save()
        return response

    except AggregateOrder.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    except Exception as e:
        print(f"Error in download_bill: {str(e)}")  # Print the error
        return HttpResponse(f"Error: {str(e)}", status=500)



# views.py

import qrcode
from django.http import HttpResponse
from io import BytesIO
from core.models import Table

def generate_qr_code(request, table_id):
    # Get the table object
    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        return HttpResponse("Table not found", status=404)
    
    # Determine scheme and host dynamically
    scheme = "https" if request.is_secure() else "http"
    #host will be below when deployed
    #host = request.get_host()
    host = "192.168.43.77:3000"
    
    # URL to be encoded into the QR code; now using '/menu'
    url = f"{scheme}://{host}/menu/{table.table_number}"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill="black", back_color="white")

    # Save the QR code image into memory
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    
    return response

