# Generated by Django 4.2.7 on 2023-11-28 13:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0032_remove_profile_first_name_remove_profile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='registration_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]