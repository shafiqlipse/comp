# Generated by Django 5.0.6 on 2024-08-08 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='shirt_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]