# Generated by Django 5.0.1 on 2024-12-04 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_menuitem_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=2),
        ),
    ]