# Generated by Django 5.1.6 on 2025-03-18 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_receiptdetail_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiptdetail',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='receiptdetail',
            name='unit_price',
        ),
    ]
