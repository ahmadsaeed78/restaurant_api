# views_multorder.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers_multorder import AggregateOrderSerializerCreate

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
    serializer = AggregateOrderSerializerCreate(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        print(order)
        # If a table is specified, update its status to booked.
        if order.table_id:
            try:
                table = Table.objects.get(id=order.table_id)
                table.is_booked = True
                table.save()
                print(f"✅ Table {table.id} is now booked.")
            except Table.DoesNotExist:
                print("❌ Table not found.")
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
    host = "frontend-brown-alpha-12.vercel.app"
    
    # URL to be encoded into the QR code; now using '/menu'
    #url = f"{scheme}://{host}/menu/{table.table_number}"
    url = f"{host}/menu/{table.table_number}"

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


# reservations/views.py
from rest_framework import generics, permissions
from .models import Reservation
from .serializers_multorder import ReservationSerializer

class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require JWT authentication

    def perform_create(self, serializer):
        # Automatically set the user (from the token) and ensure status is Pending
        serializer.save(user=self.request.user, status="Pending")



from rest_framework import generics, permissions
from .models import Reservation
from .serializers_multorder import ReservationSerializer  # adjust import if needed

class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # If the user is a chief, return all reservations.
        if user.role == 'chief':
            return Reservation.objects.all().order_by("-date")
        # Otherwise, return only reservations for the user.
        return Reservation.objects.filter(user=user).order_by("-date")
    


'''
# views.py
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Reservation, Table
from .serializers_multorder import ApproveReservationSerializer
from .tasks import assign_table_for_reservation, release_table_for_reservation


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.status.lower() != "pending":
        return Response({"error": "Reservation is not pending."}, status=status.HTTP_400_BAD_REQUEST)

    reservation.status = "Approved"
    reservation.save()

    now = timezone.now()

    # Schedule assignment 30 minutes before reservation date/time
    assign_time = timezone.make_aware(
        datetime.combine(reservation.date, reservation.time)
    ) - timedelta(minutes=30)
    delay = max(0, (assign_time - now).total_seconds())
    assign_table_for_reservation.apply_async(args=[reservation.id], countdown=delay)

    # Schedule release 1.5 hours after reservation date/time
    release_time = timezone.make_aware(
        datetime.combine(reservation.date, reservation.time)
    ) + timedelta(hours=1, minutes=30)
    delay_release = max(0, (release_time - now).total_seconds())
    release_table_for_reservation.apply_async(args=[reservation.id], countdown=delay_release)

    serializer = ApproveReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)
'''
# views.py

from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Reservation
from .serializers_multorder import ApproveReservationSerializer
from .tasks import assign_table_for_reservation, release_table_for_reservation
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.status.lower() != "pending":
        return Response({"error": "Reservation is not pending."}, status=status.HTTP_400_BAD_REQUEST)

    reservation.status = "Approved"
    reservation.save()

    # Get "now" in local timezone
    now = timezone.localtime()

    # Build the reservation datetime in local tz
    reservation_dt = timezone.make_aware(
        datetime.combine(reservation.date, reservation.time),
        timezone.get_default_timezone()
    )

    # Schedule assignment 30 minutes before reservation
    assign_time = reservation_dt - timedelta(minutes=2)
    delay_assign = max(0, (assign_time - now).total_seconds())
    print(reservation_dt)
    print(timedelta(minutes=2))
    print(assign_time)
    print(assign_time - now)
    print(now)
    print(timezone.now())
    print((assign_time - now).total_seconds())
    print(delay_assign)
    assign_table_for_reservation.apply_async(args=[reservation.id], countdown=delay_assign)

    # Schedule release 1.5 hours after reservation
    release_time = reservation_dt + timedelta(minutes=2)
    delay_release = max(0, (release_time - now).total_seconds())
    print(reservation_dt)
    print(timedelta(minutes=2))
    print(release_time)
    print(release_time - now)
    print(now)
    print((release_time - now).total_seconds())
    print(delay_release)
    release_table_for_reservation.apply_async(args=[reservation.id], countdown=delay_release)

    serializer = ApproveReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)

'''
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.status.lower() != "pending":
        return Response({"error": "Reservation is not pending."}, status=status.HTTP_400_BAD_REQUEST)

    # Mark reservation approved
    reservation.status = "Approved"
    reservation.save()

    now = timezone.now()
    # Combine date and time into a single timezone-aware datetime
    reservation_dt = timezone.make_aware(datetime.combine(reservation.date, reservation.time))

    # Schedule assignment 30 minutes before reservation
    assign_time = reservation_dt - timedelta(minutes=2)
    delay_assign = max(0, (assign_time - now).total_seconds())
    print(reservation_dt)
    print(timedelta(minutes=2))
    print(assign_time)
    print(assign_time - now)
    print(now)
    print((assign_time - now).total_seconds())
    print(delay_assign)
    assign_table_for_reservation.apply_async(args=[reservation.id], countdown=delay_assign)

    # Schedule release 1.5 hours after reservation
    release_time = reservation_dt + timedelta(minutes=2)
    delay_release = max(0, (release_time - now).total_seconds())
    print(reservation_dt)
    print(timedelta(minutes=2))
    print(release_time)
    print(release_time - now)
    print(now)
    print((release_time - now).total_seconds())
    print(delay_release)
    release_table_for_reservation.apply_async(args=[reservation.id], countdown=delay_release)

    serializer = ApproveReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)

# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Reservation
from .serializers_multorder import ApproveReservationSerializer
from .tasks import assign_table_for_reservation, release_table_for_reservation

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.status.lower() != "pending":
        return Response({"error": "Reservation is not pending."}, status=status.HTTP_400_BAD_REQUEST)

    # Mark as approved immediately
    reservation.status = "Approved"
    reservation.save()

    # === TEST SCHEDULING ===
    # Assign table 2 minutes after approval
    assign_table_for_reservation.apply_async(args=[reservation.id], countdown=1 * 60)
    # Release table 4 minutes after approval
    release_table_for_reservation.apply_async(args=[reservation.id], countdown=2 * 60)
    # ========================

    serializer = ApproveReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)
'''




# views.py
from rest_framework import generics
from .models import Table
from .serializers_multorder import TableStatusSerializer

class TableStatusUpdateAPIView(generics.UpdateAPIView):
    """
    API endpoint for updating the table status.
    Expects PATCH requests to update the `is_booked` field.
    """
    queryset = Table.objects.all()
    serializer_class = TableStatusSerializer
    lookup_field = 'id'

from .models import DeliveryOrder, DeliveryOrderItem
from .serializers_multorder import DeliveryOrderSerializer, DeliveryOrderSerializerCreate

@api_view(['POST'])
def create_delivery_order(request):
    """
    API endpoint to create a multi-item delivery order.
    Expected payload:
    {
        "user": 1,  # optional, if registered
        "customer_name": "John Doe",
        "address": "123 Main St, City",
        "phone_number": "1234567890",
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
    serializer = DeliveryOrderSerializerCreate(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response(DeliveryOrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryOrderListAPIView(generics.ListAPIView):
    queryset = DeliveryOrder.objects.all().order_by('-created_at')
    serializer_class = DeliveryOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryOrderRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DeliveryOrder.objects.all()
    serializer_class = DeliveryOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_delivery_order_status(request, order_id):
    order = get_object_or_404(DeliveryOrder, id=order_id)
    new_status = request.data.get("status")
    if new_status not in ["Delivered", "Completed", "Paid"]:
        return Response({"error": "Invalid status update"}, status=status.HTTP_400_BAD_REQUEST)
    order.status = new_status
    order.save()
    return Response({"message": "Order status updated", "order": DeliveryOrderSerializer(order).data})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_delivery_bill(request, order_id):
    try:
        order = DeliveryOrder.objects.get(id=order_id)
        items = DeliveryOrderItem.objects.filter(order=order)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="delivery_bill_{order_id}.pdf"'
        pdf = canvas.Canvas(response)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 800, "Restaurant Delivery Bill")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 770, f"Order ID: {order.id}")
        pdf.drawString(100, 750, f"Customer: {order.customer_name}")
        pdf.drawString(100, 735, f"Address: {order.address}")
        pdf.drawString(100, 720, f"Phone: {order.phone_number}")
        pdf.drawString(100, 700, f"Total Price: Rs.{order.total_price}")
        pdf.drawString(100, 680, "Items Ordered:")
        y_position = 660
        for item in items:
            pdf.drawString(120, y_position, f"- {item.menu_item.name} x {item.quantity}")
            y_position -= 20
        pdf.save()
        return response
    except DeliveryOrder.DoesNotExist:
        return HttpResponse("Order not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
