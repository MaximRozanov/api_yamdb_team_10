# Generated by Django 3.2 on 2024-10-03 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='titles',
            old_name='genres',
            new_name='genre',
        ),
        migrations.AddField(
            model_name='titles',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
