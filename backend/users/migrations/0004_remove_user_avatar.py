# Generated by Django 5.1.7 on 2025-03-29 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
    ]
