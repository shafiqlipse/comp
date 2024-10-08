# Generated by Django 5.0.6 on 2024-06-30 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('dashboard', '0002_alter_schoolteam_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Athletics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('MIXED', 'Mixed')], max_length=10, null=True)),
                ('age', models.CharField(blank=True, choices=[('U16', 'U16'), ('U18', 'U18'), ('U20', 'U20')], max_length=10, null=True)),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.championship')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.season')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.sport')),
                ('teams', models.ManyToManyField(related_name='ateams', to='dashboard.schoolteam')),
            ],
        ),
        migrations.CreateModel(
            name='AthleticsEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('event_type', models.CharField(choices=[('TRACK', 'Track'), ('FIELD', 'Field'), ('COMBINED', 'Combined')], max_length=50)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('MIXED', 'Mixed')], max_length=10)),
                ('venue', models.CharField(blank=True, max_length=10, null=True)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('athletes', models.ManyToManyField(related_name='events_athletes', to='accounts.athlete')),
                ('team', models.ManyToManyField(related_name='events_team', to='dashboard.schoolteam')),
            ],
        ),
        migrations.CreateModel(
            name='AthleticsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_seconds', models.FloatField()),
                ('position', models.IntegerField(blank=True, null=True)),
                ('athlete', models.ManyToManyField(related_name='results_athlete', to='accounts.athlete')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='athletics.athleticsevent')),
                ('team', models.ManyToManyField(related_name='results_team', to='dashboard.schoolteam')),
            ],
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('GOLD', 'Gold'), ('SILVER', 'Silver'), ('BRONZE', 'Bronze')], max_length=10)),
                ('date', models.DateField()),
                ('athlete', models.ManyToManyField(related_name='medal_athletes', to='accounts.athlete')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='athletics.athleticsevent')),
                ('team', models.ManyToManyField(related_name='medal_team', to='dashboard.schoolteam')),
            ],
        ),
    ]
