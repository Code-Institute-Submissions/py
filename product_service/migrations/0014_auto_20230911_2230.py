# Generated by Django 3.2.20 on 2023-09-11 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_service', '0013_auto_20230910_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=528),
        ),
        migrations.AlterField(
            model_name='product',
            name='excerpt',
            field=models.CharField(max_length=264),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(max_length=528),
        ),
        migrations.AlterField(
            model_name='service',
            name='excerpt',
            field=models.CharField(max_length=264),
        ),
    ]
