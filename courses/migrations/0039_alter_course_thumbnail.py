# Generated by Django 4.2.7 on 2023-11-28 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0038_alter_course_thumbnail_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(upload_to='courses/   thumbnail'),
        ),
    ]
