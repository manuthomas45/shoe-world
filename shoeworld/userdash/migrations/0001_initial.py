# Generated by Django 5.0.6 on 2024-08-09 05:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('house_name', models.CharField(max_length=500)),
                ('street_name', models.CharField(max_length=500)),
                ('pin_number', models.IntegerField()),
                ('district', models.CharField(max_length=300)),
                ('state', models.CharField(max_length=300)),
                ('country', models.CharField(default='null', max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('order_status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
