# Generated by Django 4.2.6 on 2023-11-06 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_floodedimage_segmented_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='floodedimage',
            name='segmented_image',
            field=models.ImageField(default='', upload_to='mask'),
            preserve_default=False,
        ),
    ]