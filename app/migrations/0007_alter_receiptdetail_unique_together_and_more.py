# Generated by Django 5.1.6 on 2025-03-18 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_receiptdetail_unit_price'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='receiptdetail',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='receiptdetail',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
        migrations.AlterField(
            model_name='receiptdetail',
            name='receipt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.receipt'),
        ),
    ]
