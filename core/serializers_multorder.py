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
