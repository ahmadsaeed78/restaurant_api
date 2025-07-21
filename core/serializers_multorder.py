# serializers_multorder.py

from rest_framework import serializers
from .models import AggregateOrder, AggregateOrderItem
from .models import MenuItem  # If you want to include menu item details

class AggregateOrderItemSerializer(serializers.ModelSerializer):
    # Optionally, include some details from the MenuItem model
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = AggregateOrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'special_instructions']

class AggregateOrderSerializer(serializers.ModelSerializer):
    items = AggregateOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = AggregateOrder
        fields = [
            'id',
            'user',
            'table',
            'total_price',
            'status',
            'created_at',
            'items'
        ]



from .models import Reservation

# reservations/serializers.py
from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'date', 'time', 'guests', 'status']
        read_only_fields = ('status', 'user')




from rest_framework import serializers
from .models import Reservation, Table

class ApproveReservationSerializer(serializers.ModelSerializer):
    # Show the assigned table's PK and its human-readable number
    table = serializers.PrimaryKeyRelatedField(read_only=True)
    table_number = serializers.CharField(source='table.table_number', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id',
            'user',
            'date',
            'time',
            'guests',
            'status',
            'table',
            'table_number',
        ]
        read_only_fields = ('status', 'user', 'table')







class AggregateOrderSerializerCreate(serializers.ModelSerializer):
    items = AggregateOrderItemSerializer(many=True)

    class Meta:
        model = AggregateOrder
        fields = [
            'id', 
            'user', 
            'table', 
            'customer_name', 
            'total_price', 
            'status', 
            'created_at', 
            'items'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = AggregateOrder.objects.create(**validated_data)
        total_price = 0

        # Create each AggregateOrderItem and calculate total price.
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data.get('quantity', 1)
            AggregateOrderItem.objects.create(order=order, **item_data)
            total_price += menu_item.price * quantity
        
        # Update the total price in the order.
        order.total_price = total_price
        order.save()
        return order






# serializers.py
from rest_framework import serializers
from .models import Table

class TableStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'is_booked']  # Expose table id and booking status.
        read_only_fields = ['id']

from .models import DeliveryOrder, DeliveryOrderItem

class DeliveryOrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = DeliveryOrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'special_instructions']

class DeliveryOrderSerializer(serializers.ModelSerializer):
    items = DeliveryOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = DeliveryOrder
        fields = [
            'id',
            'user',
            'customer_name',
            'address',
            'phone_number',
            'total_price',
            'status',
            'created_at',
            'items'
        ]

class DeliveryOrderSerializerCreate(serializers.ModelSerializer):
    items = DeliveryOrderItemSerializer(many=True)

    class Meta:
        model = DeliveryOrder
        fields = [
            'id',
            'user',
            'customer_name',
            'address',
            'phone_number',
            'total_price',
            'status',
            'created_at',
            'items'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = DeliveryOrder.objects.create(**validated_data)
        total_price = 0
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data.get('quantity', 1)
            DeliveryOrderItem.objects.create(order=order, **item_data)
            total_price += menu_item.price * quantity
        order.total_price = total_price
        order.save()
        return order
