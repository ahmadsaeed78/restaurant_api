# Generated by Django 5.0.1 on 2024-12-04 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_unregisteredorder_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1),
        ),
    ]
