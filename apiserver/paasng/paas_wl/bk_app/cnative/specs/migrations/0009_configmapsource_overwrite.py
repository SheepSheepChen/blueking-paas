# Generated by Django 4.2.16 on 2025-01-03 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0008_auto_20240327_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='configmapsource',
            name='overwrite',
            field=models.BooleanField(default=False, help_text='是否覆盖目录下的文件'),
        ),
    ]
