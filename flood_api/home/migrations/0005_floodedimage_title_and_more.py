# Generated by Django 4.2.6 on 2023-10-31 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_floodedimage_coordinates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='floodedimage',
            name='title',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='floodedimage',
            name='prediction_data',
            field=models.JSONField(default={}),
        ),
    ]