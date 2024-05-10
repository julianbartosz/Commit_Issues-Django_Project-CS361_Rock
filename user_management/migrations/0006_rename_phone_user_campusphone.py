# Generated by Django 5.0.4 on 2024-05-04 08:38

from django.db import migrations, models


def generate_unique_emplid(apps, schema_editor):
    User = apps.get_model('user_management', 'User')
    for user in User.objects.all():
        user.emplid = str(user.id)  # replace with your own unique value generation logic
        user.save()


def generate_unique_epantherid(apps, schema_editor):
    User = apps.get_model('user_management', 'User')
    for user in User.objects.all():
        user.epantherid = 'e' + str(user.id)  # replace with your own unique value generation logic
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_remove_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='building_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='building name'),
        ),
        migrations.AddField(
            model_name='user',
            name='classification',
            field=models.CharField(blank=True, max_length=50, verbose_name='classification'),
        ),
        migrations.AddField(
            model_name='user',
            name='emplid',
            field=models.CharField(max_length=10, unique=True, null=True, verbose_name='emplid'),
        ),
        migrations.RunPython(generate_unique_emplid),
        migrations.AlterField(
            model_name='user',
            name='emplid',
            field=models.CharField(max_length=10, unique=True, verbose_name='emplid'),
        ),
        migrations.AddField(
            model_name='user',
            name='epantherid',
            field=models.CharField(max_length=20, unique=True, null=True, verbose_name='ePanther ID'),
        ),
        migrations.RunPython(generate_unique_epantherid),
        migrations.AlterField(
            model_name='user',
            name='epantherid',
            field=models.CharField(max_length=20, unique=True, verbose_name='ePanther ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='person_id',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='person ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='room_number',
            field=models.CharField(blank=True, max_length=10, verbose_name='room number'),
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.CharField(blank=True, max_length=100, verbose_name='school'),
        ),
        migrations.AddField(
            model_name='user',
            name='year_in_school',
            field=models.CharField(blank=True, max_length=20, verbose_name='year in school'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Supervisor', 'Supervisor/Administrator'), ('Instructor', 'Instructor'), ('TA', 'Teaching Assistant'), ('Student', 'Student')], default='TA', help_text='User role in the system', max_length=50, verbose_name='role'),
        ),
    ]