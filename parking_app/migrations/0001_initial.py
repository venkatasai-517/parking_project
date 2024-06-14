# Generated by Django 5.0.1 on 2024-01-31 09:56

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_area_number', models.CharField(max_length=10)),
                ('vehicle_type', models.CharField(max_length=30)),
                ('vehicle_limit', models.CharField(max_length=20)),
                ('parking_charge', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('activated', 'Activated'), ('deactivated', 'Deactivated')], default='activated', max_length=20)),
                ('doc', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='vehicle_entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_no', models.CharField(max_length=11)),
                ('vehicle_type', models.CharField(max_length=30)),
                ('parking_charge', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('parked', 'Parked'), ('leaved', 'Leaved')], default='parked', max_length=20)),
                ('arrival_time', models.DateTimeField(default=datetime.datetime.now)),
                ('parking_area_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.category')),
            ],
        ),
    ]
