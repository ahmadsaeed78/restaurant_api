from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('chief', 'Chief'),
        ('admin', 'Admin'),
    )
    
    name = models.CharField(max_length=255, null=True, blank=True)  # Add name field
    email = models.EmailField(unique=True)  # Ensure email is unique
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add phone number field
    
    # Override groups and user_permissions with unique related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_groups',  # Add unique related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions',  # Add unique related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.name
    

class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MenuGroup(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    parent_group = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_groups')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

import random
class MenuItem(models.Model):
    menugroup = models.ForeignKey(MenuGroup, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    available = models.BooleanField(default=True)
    rating = models.IntegerField(default=random.randint(1, 5), choices=[(i, str(i)) for i in range(1, 6)])  # Rating between 1 and 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ordered')
    created_at = models.DateTimeField(auto_now_add=True)


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    is_booked = models.BooleanField(default=False)  # Status: Booked or Not

    def __str__(self):
        return f"Table {self.table_number} - {'Booked' if self.is_booked else 'Available'}"

class UnregisteredOrder(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customer_name = models.CharField(max_length=255)
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True)
    order_time = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('ordered', 'Ordered'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('pain', 'Paid')
    ]
    status = models.CharField(
        max_length=10,
        choices=status_choices,
        default='ordered'
    )

    def __str__(self):
        return f"Order: {self.menu_item.name} (Table {self.table.table_number if self.table else 'N/A'}) (Status: {self.get_status_display()})"



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"
    







#new addition
    # models_multorder.py

from django.db import models
from django.conf import settings  # to reference your custom User model
from .models import MenuItem, Table  # Import existing models

class AggregateOrder(models.Model):
    """
    Represents a multi-item order (e.g., a cart order).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )  # For registered users; can be null for guest orders.
    table = models.ForeignKey(
        Table, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )  # Optional reference for table orders.
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status_choices = [
        ('ordered', 'Ordered'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
    ]
    status = models.CharField(
        max_length=10, 
        choices=status_choices, 
        default='ordered'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AggregateOrder {self.id} - {self.customer_name or 'Guest'}"

class AggregateOrderItem(models.Model):
    """
    Represents individual items within an AggregateOrder.
    """
    order = models.ForeignKey(
        AggregateOrder, 
        related_name="items", 
        on_delete=models.CASCADE
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order {self.order.id})"



class Reservation(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)  # Initially null

    def __str__(self):
        return f"Reservation for {self.user} on {self.date} at {self.time}"