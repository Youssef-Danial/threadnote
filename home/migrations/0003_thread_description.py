# Generated by Django 5.0.1 on 2024-02-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_note_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='description',
            field=models.TextField(blank=True, max_length=256),
        ),
    ]