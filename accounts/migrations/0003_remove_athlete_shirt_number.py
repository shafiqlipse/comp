# Generated by Django 5.0.6 on 2024-09-02 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_athlete_date_of_birth_athlete_shirt_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='shirt_number',
        ),
    ]