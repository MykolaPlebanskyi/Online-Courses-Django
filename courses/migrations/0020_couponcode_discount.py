# Generated by Django 4.2.7 on 2023-11-26 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_couponcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcode',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
