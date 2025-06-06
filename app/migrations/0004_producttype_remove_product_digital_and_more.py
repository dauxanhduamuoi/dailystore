# Generated by Django 5.1.6 on 2025-03-16 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_order_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.producttype'),
        ),
    ]
