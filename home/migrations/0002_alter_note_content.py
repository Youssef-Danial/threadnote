# Generated by Django 5.0.1 on 2024-02-03 16:07

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='content',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]