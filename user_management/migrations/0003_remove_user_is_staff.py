# Generated by Django 5.0.4 on 2024-04-22 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_alter_user_managers_remove_user_date_joined_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
