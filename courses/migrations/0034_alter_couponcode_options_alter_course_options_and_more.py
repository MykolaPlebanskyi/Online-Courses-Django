# Generated by Django 4.2.7 on 2023-11-28 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0033_profile_registration_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='couponcode',
            options={'verbose_name': 'Купони', 'verbose_name_plural': 'Купони'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Курси', 'verbose_name_plural': 'Курси'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Питання', 'verbose_name_plural': 'Питання'},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name': 'Тести', 'verbose_name_plural': 'Тести'},
        ),
        migrations.AlterModelOptions(
            name='usercourse',
            options={'verbose_name': 'Курси користувачів', 'verbose_name_plural': 'Курси користувачів'},
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='status',
            field=models.CharField(choices=[('Active', 'Активний'), ('Complete', 'Пройдений')], default='Active', max_length=10),
        ),
    ]
