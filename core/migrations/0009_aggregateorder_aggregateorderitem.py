# Generated by Django 5.0.1 on 2025-03-30 19:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_contact_alter_menuitem_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregateOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('status', models.CharField(choices=[('ordered', 'Ordered'), ('delivered', 'Delivered'), ('completed', 'Completed'), ('paid', 'Paid')], default='ordered', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.table')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AggregateOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('special_instructions', models.TextField(blank=True, null=True)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.aggregateorder')),
            ],
        ),
    ]
