# Generated by Django 3.2.20 on 2023-09-27 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20230926_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[('0', 'Pending'), ('1', 'Cancelled'), ('2', 'Completed')], default=0),
        ),
    ]