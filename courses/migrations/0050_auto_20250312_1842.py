# Generated by Django 3.1.4 on 2025-03-12 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0049_auto_20250312_1828'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placementanswer',
            options={},
        ),
        migrations.RemoveField(
            model_name='placementquestion',
            name='level',
        ),
        migrations.AddField(
            model_name='placementtest',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('uk', 'Ukrainian'), ('es', 'Spanish'), ('de', 'German')], default='en', max_length=2),
        ),
    ]
