from rest_framework import serializers
'''
from .models import User, Menu, MenuItem, Reservation, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'menu', 'name', 'price', 'description', 'available']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'date', 'time', 'guests', 'status']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'status']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']  # Include fields relevant to your model

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
'''


#main Serializers
from rest_framework import serializers
from .models import User, Menu, MenuGroup, MenuItem, Reservation, Order, Table, UnregisteredOrder

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'role', 'phone_number']

# Menu serializer
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'image', 'is_active', 'created_at', 'updated_at']

# Menu Group serializer
class MenuGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuGroup
        fields = ['id', 'menu', 'name', 'description', 'parent_group', 'is_active', 'image', 'created_at', 'updated_at']

# Menu Item serializer
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'menugroup', 'name', 'price', 'description', 'image', 'available', 'rating', 'created_at', 'updated_at']

# Reservation serializer
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'date', 'time', 'guests', 'status']

# Order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'menu_item', 'quantity', 'status', 'created_at']

# Table serializer
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'is_booked']

# Unregistered Order serializer
class UnregisteredOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnregisteredOrder
        fields = ['id', 'menu_item', 'quantity', 'customer_name', 'table', 'order_time', 'status']



#generate herirchy response
from rest_framework import serializers
from .models import Menu, MenuGroup, MenuItem

class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'image', 'available']

class MenuGroupsSerializer(serializers.ModelSerializer):
    items = MenuItemsSerializer(many=True, read_only=True)  # Nested MenuItem serializer

    class Meta:
        model = MenuGroup
        fields = ['id', 'name', 'description', 'image', 'items']

class MenusSerializer(serializers.ModelSerializer):
    groups = MenuGroupsSerializer(many=True, read_only=True)  # Nested MenuGroup serializer

    class Meta:
        model = Menu
        fields = ['id', 'name', 'description','image' , 'groups']




#two level herirchy pass
class MenuItemTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'image', 'available', 'rating']

class MenuGroupTwoSerializer(serializers.ModelSerializer):
    items = MenuItemTwoSerializer(many=True, read_only=True)  # Nest MenuItems here

    class Meta:
        model = MenuGroup
        fields = ['id', 'name', 'description', 'image', 'items']





from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'phone_no', 'message']

# User Registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'phone_number', 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user