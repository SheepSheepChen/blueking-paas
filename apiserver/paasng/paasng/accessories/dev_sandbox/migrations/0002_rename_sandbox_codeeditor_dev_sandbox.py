# Generated by Django 3.2.25 on 2024-10-23 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dev_sandbox', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codeeditor',
            old_name='sandbox',
            new_name='dev_sandbox',
        ),
    ]