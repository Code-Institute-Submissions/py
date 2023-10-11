# Generated by Django 3.2.20 on 2023-10-09 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Suspended'), (2, 'Active')], default=0),
        ),
        migrations.AddField(
            model_name='like',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Suspended'), (2, 'Active')], default=0),
        ),
    ]