# Generated by Django 5.1.6 on 2025-03-18 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_receiptdetail_subtotal_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReceiptDetail',
        ),
    ]
