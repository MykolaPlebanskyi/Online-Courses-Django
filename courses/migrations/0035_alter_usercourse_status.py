# Generated by Django 4.2.7 on 2023-11-28 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0034_alter_couponcode_options_alter_course_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='status',
            field=models.CharField(choices=[('Active', 'Активний'), ('Complete', 'Завершений')], default='Active', max_length=10),
        ),
    ]
