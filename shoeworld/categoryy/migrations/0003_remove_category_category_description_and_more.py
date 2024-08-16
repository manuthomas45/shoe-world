# Generated by Django 5.0.6 on 2024-07-18 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoryy', '0002_alter_category_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='is_available',
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(max_length=50),
        ),
    ]
