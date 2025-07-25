from django.urls import reverse
from rest_framework import viewsets
'''
from .models import Menu, MenuItem, Reservation, Order
from .serializers import MenuSerializer, MenuItemSerializer, ReservationSerializer, OrderSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

'''



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#pages
from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')

def reservation(request):
    return render(request, 'reservation.html')

def contact(request):
    return render(request, 'contact.html')

def login_user(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')



from .models import MenuItem

def menu_view(request):
    menu_items = MenuItem.objects.filter(available=True)  # Fetch all menu items from the database
    context = {
        'menu_items': menu_items
    }
    return render(request, 'menu.html', context)

from .forms import ReservationForm
from .models import Reservation


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from .models import Reservation
from .decorators import chief_required, customer_required, admin_required

@customer_required
def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('success_page')
    else:
        form = ReservationForm()
    
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation.html', {'form': form, 'reservations': reservations})


    
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logging out

def reserve_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Save data to the database
            return redirect('reservation')
    return redirect('reservation')


from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SignUpForm

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Log the user in after signup
            if user.role == 'customer':
                return render(request, 'customer_dashboard.html', {'user': user})  # Change this to your desired redirect
            elif user.role == 'chief':
                return redirect('chief_dashboard')  # Change this to your desired redirect
            elif user.role == 'admin':
                return redirect('admin_dashboard')  # Change this to your desired redirect
            else:
                return redirect('home')  # Change this to your desired redirect
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                if user.role == 'customer':
                    return render(request, 'customer_dashboard.html', {'user': user})  # Change this to your desired redirect
                elif user.role == 'chief':
                    return redirect('chief_dashboard')  # Change this to your desired redirect
                elif user.role == 'admin':
                    return redirect('admin_dashboard')  # Change this to your desired redirect
                else:
                    return redirect('home')  # Change this to your desired redirect
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')  # Make sure this template exists



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User

@customer_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

@admin_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .forms import MenuItemForm  # We'll create this form in the next step
@chief_required
def chief_dashboard(request):
    return render(request, 'chief_dashboard.html')

@chief_required
def menu_management(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu_management.html', {'menu_items': menu_items})

@chief_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form with the menu field set
            return redirect('menu_management')  # Redirect to the menu list page after adding
    else:
        form = MenuItemForm()

    return render(request, 'add_menu_item.html', {'form': form})


@chief_required
def update_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_management')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'update_menu_item.html', {'form': form})

@chief_required
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('menu_management')
    return render(request, 'delete_menu_item.html', {'item': item})





# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu, MenuGroup
from .forms import MenuForm, MenuGroupForm

# Menu Views
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'chief/menu_list.html', {'menus': menus})

def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'chief/add_menu.html', {'form': form})

def update_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)

#menu have data or null


    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'chief/update_menu.html', {'form': form})

def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    return redirect('menu_list')

# MenuGroup Views
def menu_group_list(request):
    menu_groups = MenuGroup.objects.all()
    return render(request, 'chief/menu_group_list.html', {'menu_groups': menu_groups})

def add_menu_group(request):
    if request.method == 'POST':
        form = MenuGroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_group_list')
    else:
        form = MenuGroupForm()
    return render(request, 'chief/add_menu_group.html', {'form': form})

def update_menu_group(request, menu_group_id):
    menu_group = get_object_or_404(MenuGroup, id=menu_group_id)
    if request.method == 'POST':
        form = MenuGroupForm(request.POST, request.FILES, instance=menu_group)
        if form.is_valid():
            form.save()
            return redirect('menu_group_list')
    else:
        form = MenuGroupForm(instance=menu_group)
    return render(request, 'chief/update_menu_group.html', {'form': form})

def delete_menu_group(request, menu_group_id):
    menu_group = get_object_or_404(MenuGroup, id=menu_group_id)
    menu_group.delete()
    return redirect('menu_group_list')




def manage_unregistered_orders(request):
    orders = UnregisteredOrder.objects.all().order_by('-order_time')
    return render(request, 'manage_unregistered_orders.html', {'orders': orders})

def change_status(request, order_id, new_status):
    order = get_object_or_404(UnregisteredOrder, id=order_id)

    if new_status not in ['delivered', 'completed', 'paid']:
        messages.error(request, "Invalid status change.")
        return redirect('manage_unregistered_orders')
    
    if new_status == 'paid':
        table = order.table
        table.is_booked = False
        table.save()
    order.status = new_status
    order.save()
   

    messages.success(request, f"Order status updated to {new_status.capitalize()}.")
    return redirect('manage_unregistered_orders')


#bill generations
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import UnregisteredOrder
from .utils import generate_pdf_bill, generate_pdf_bill_v2  # If you have the function in a separate utils.py file

def generate_bill(request, order_id):
    # Get the order details
    order = get_object_or_404(UnregisteredOrder, id=order_id)
    
    if order.status != 'completed':
        messages.error(request, "Only completed orders can generate a bill.")
        return redirect('manage_unregistered_orders')
    
    # Generate PDF
    pdf_buffer = generate_pdf_bill_v2(order)
    
    # Return PDF as an HTTP response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="bill_order_{order.id}.pdf"'
    return response



def scan_menu(request):
    menu_items = MenuItem.objects.filter(available=True)
    table_number = request.GET.get('table_id')
    table = get_object_or_404(Table, id=table_number)
    return render(request, 'scan_menu.html', {'menu_items': menu_items, 'table': table})

from .models import Table, UnregisteredOrder

def place_order_unregistered(request, item_id, table_id):
    item = get_object_or_404(MenuItem, id=item_id)
    tables = Table.objects.filter(is_booked = False)
    table_number = table_id

    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        table_id = request.POST['table']
        quantity = int(request.POST['quantity'])
        
        
        try:
            table = Table.objects.get(id=table_id)

            # Create the order
            UnregisteredOrder.objects.create(
                customer_name=customer_name,
                menu_item=item,
                table=table,
                quantity=quantity,
            )

            # Mark table as booked
            table.is_booked = True
            table.save()

            # Add a success message
            messages.success(request, "Order placed successfully!")
        except Exception as e:
            # Add a failure message
            messages.error(request, f"Failed to place order: {str(e)}")

        return redirect(f"/scan-menu/?table_id={table_number}")  # Redirect to scan-menu page

    return render(request, 'place_order_unregistered.html', {'item': item, 'tables': tables, 'table_number': table_number})




from django.shortcuts import render, get_object_or_404
from .models import Table
from django.http import JsonResponse
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def manage_tables_chief(request):
    tables = Table.objects.all()
    return render(request, 'chief/manage_tables_chief.html', {'tables': tables})

def generate_table_qr(request, table_id):
    table = Table.objects.get(id=table_id)
    url = request.build_absolute_uri(reverse('scan_menu') + f"?table_number={table.table_number}")
    url_api = "localhost:3000/menus/" + f"{table.table_number}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_api)
    qr.make(fit=True)

    # Create an image of the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response




from django.shortcuts import redirect, get_object_or_404
from .models import MenuItem
@chief_required
def toggle_availability(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_management')  # Redirect to the menu list after toggling

@chief_required
def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'orders': orders})

@chief_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    if new_status in ['delivered', 'completed']:
        order.status = new_status
        order.save()
    return redirect('manage_orders')











from .models import MenuItem, Order
from .forms import OrderForm

def place_order(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.menu_item = menu_item
            order.status = 'ordered'
            order.save()
            return redirect('menu')
    else:
        form = OrderForm()
    
    return render(request, 'place_order.html', {'menu_item': menu_item, 'form': form})



#admin dashboard
def manage_tables(request):
    tables = Table.objects.all()
    return render(request, 'admin/manage_tables.html', {'tables': tables})

def add_table(request):
    if request.method == "POST":
        table_number = request.POST.get('table_number')
        if Table.objects.filter(table_number=table_number).exists():
            messages.error(request, "Table number already exists!")
        else:
            Table.objects.create(table_number=table_number)
            messages.success(request, "Table added successfully!")
        return redirect('manage_tables')
    return render(request, 'admin/add_table.html')


def delete_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    table.delete()
    messages.success(request, "Table deleted successfully!")
    return redirect('manage_tables')



#API views
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Menu, MenuGroup, MenuItem, Reservation, Order, Table, UnregisteredOrder
from .serializers import UserSerializer, MenuSerializer, MenuGroupSerializer, MenuItemSerializer, ReservationSerializer, OrderSerializer, TableSerializer, UnregisteredOrderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from rest_framework.response import Response

# User Views
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Menu, MenuGroup, MenuItem
from .serializers import MenuSerializer, MenuGroupSerializer, MenuItemSerializer

# Menu Views
class MenuListCreateAPIView(ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class MenuRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Menu.DoesNotExist:
            return Response({"error": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

# MenuGroup Views
class MenuGroupListCreateAPIView(ListCreateAPIView):
    queryset = MenuGroup.objects.all()
    serializer_class = MenuGroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class MenuGroupRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MenuGroup.objects.all()
    serializer_class = MenuGroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MenuGroup.DoesNotExist:
            return Response({"error": "Menu group not found."}, status=status.HTTP_404_NOT_FOUND)

# MenuItem Views
class MenuItemListCreateAPIView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Public read, authenticated write

    def perform_create(self, serializer):
        serializer.save()

class MenuItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Menu
from .serializers import MenusSerializer

class MenuListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        menus = Menu.objects.filter(is_active=True)  # Fetch only active menus
        # Pass the request context to the serializer
        serializer = MenusSerializer(menus, many=True, context={'request': request})
        return Response(serializer.data)

    

from .serializers import MenuGroupTwoSerializer
from rest_framework.generics import ListAPIView
#two level herirchy pass
class MenuGroupHierarchyView(ListAPIView):
    queryset = MenuGroup.objects.prefetch_related('items').filter(is_active=True)
    serializer_class = MenuGroupTwoSerializer
    permission_classes = [AllowAny]  # Public access


# Reservation Views
class ReservationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

class ReservationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

# Order Views
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

# Table Views
class TableListCreateAPIView(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

class TableRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

# Unregistered Order Views
class UnregisteredOrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = UnregisteredOrder.objects.all()
    serializer_class = UnregisteredOrderSerializer
    def perform_create(self, serializer):
        # Save the order instance
        instance = serializer.save()
        
        # Update the table's is_booked field
        if instance.table:
            table = instance.table
            table.is_booked = True
            table.save()

class UnregisteredOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnregisteredOrder.objects.all()
    serializer_class = UnregisteredOrderSerializer
    permission_classes = [IsAuthenticated]



#get all tables
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Table
from .serializers import TableSerializer

class TableListAPIView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve all tables.
        """
        tables = Table.objects.all()  # Fetch all tables from the database
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)
    


from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer

class ContactAPIView(APIView):
    permission_classes = [AllowAny]  # Allow unrestricted access

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contact information saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Check if both fields are provided
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # Generate JWT token for the user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Return the access token and role
            return Response(
                {
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
                    "role": user.role,  # Return user role
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import status

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Ensure that the user is authenticated
def update_item_availability(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)
    except MenuItem.DoesNotExist:
        return Response({"detail": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get the new availability status from the request data
    available_status = request.data.get('available')

    if available_status is None:
        return Response({"detail": "'available' field is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Update the 'available' field only
    item.available = available_status
    item.save()

    # Return the updated item
    return Response({"id": item.id, "available": item.available}, status=status.HTTP_200_OK)





#manage unregistered orders apis
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UnregisteredOrder
from .serializers import UnregisteredOrderSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_unregistered_orders(request):
    orders = UnregisteredOrder.objects.all()
    serializer = UnregisteredOrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def change_order_status(request, order_id, new_status):
    try:
        order = UnregisteredOrder.objects.get(id=order_id)
        order.status = new_status
        order.save()
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def generate_bill(request, order_id):
    try:
        order = UnregisteredOrder.objects.get(id=order_id)
        total_price = order.menu_item.price * order.quantity
        return Response({
            "customer_name": order.customer_name,
            "menu_item": order.menu_item.name,
            "quantity": order.quantity,
            "total_price": total_price
        }, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)



# views.py in Django

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MenuItem

class MenuItemList(APIView):
    def get(self, request):
        menu_items = MenuItem.objects.all().values("name", "price", "description", "image")
        return Response(menu_items)





from rest_framework.views import APIView
from rest_framework.response import Response
import joblib, os, pandas as pd

class RecommendFoodByWeather(APIView):
    def get(self, request):
        weather = request.query_params.get('weather')  # e.g. "Summer"
        if not weather:
            return Response({"error": "Weather not provided"}, status=400)

        # Load model
        base = os.path.dirname(os.path.abspath(__file__)) + "/model/"
        model = joblib.load(base + "food_weather_model.pkl")
        vectorizer = joblib.load(base + "tfidf_vectorizer.pkl")
        label_encoder = joblib.load(base + "label_encoder.pkl")

        # Load the menu items
        menu_df = pd.read_csv(base + "menu_weather_data.csv")
        menu_df['text'] = menu_df['name'] + " " + menu_df['description']

        # Predict weather label
        weather_label = label_encoder.transform([weather])[0]

        # Predict for all items
        X = vectorizer.transform(menu_df['text'])
        preds = model.predict(X)

        # Filter items matching predicted weather
        recommended = menu_df[preds == weather_label]

        return Response(recommended[['name', 'description', 'weather']].to_dict(orient="records"))

from rest_framework.generics import ListAPIView
from .serializers import ContactSerializer

class TestimonialListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Contact.objects.all().order_by('-id')  # latest first
    serializer_class = ContactSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for obj in queryset:
            data.append({
                'name': obj.name,
                'subject': obj.subject,
                'message': obj.message,
                'avatar': '/static/avatar.png'  # static avatar path, update as needed
            })
        return Response(data)
