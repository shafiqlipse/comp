# Generated by Django 5.0.6 on 2024-07-31 04:24

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
            name='R15Fixture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(blank=True, choices=[('Group', 'Group'), ('Knockout', 'Knockout')], max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('InPlay', 'InPlay'), ('Complete', 'Complete'), ('Postponed', 'Postponed')], default='Pending', max_length=100, null=True)),
                ('round', models.CharField(blank=True, max_length=100, null=True)),
                ('venue', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('team1_score', models.IntegerField(blank=True, null=True)),
                ('team2_score', models.IntegerField(blank=True, null=True)),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rug15fix', to='dashboard.season')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r15team1', to='dashboard.schoolteam')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r15team2', to='dashboard.schoolteam')),
            ],
        ),
        migrations.CreateModel(
            name='MatchEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('Try', 'Try'), ('Conversion', 'Conversion'), ('PenaltyTry', 'Penalty Try'), ('PenaltyKick', 'Penalty Kick'), ('DropGoal', 'Drop Goal'), ('Turnover', 'Turnover'), ('Lineout', 'Lineout'), ('Scrum', 'Scrum'), ('Tackle', 'Tackle'), ('Penalty', 'Penalty'), ('YellowCard', 'Yellow Card'), ('RedCard', 'Red Card'), ('Substitution', 'Substitution'), ('Injury', 'Injury'), ('KickOff', 'Kick Off'), ('HalfTime', 'Half Time'), ('FullTime', 'Full Time')], max_length=20)),
                ('minute', models.IntegerField()),
                ('commentary', models.TextField(blank=True, null=True)),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r15player', to='accounts.athlete')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r15team', to='dashboard.schoolteam')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rugby15s.r15fixture')),
            ],
        ),
        migrations.CreateModel(
            name='match_official',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_role', models.CharField(blank=True, choices=[('Referee', 'Referee'), ('Umpire', 'Umpire'), ('First assistant', 'First assistant '), ('Second assistant', 'Second assistant '), ('4th Official', '4th Official')], max_length=100, null=True)),
                ('official', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r15official', to='dashboard.official')),
                ('fixture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r15ofix', to='rugby15s.r15fixture')),
            ],
        ),
        migrations.CreateModel(
            name='R15Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('teams', models.ManyToManyField(to='dashboard.schoolteam')),
            ],
        ),
        migrations.AddField(
            model_name='r15fixture',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rugby15s.r15group'),
        ),
        migrations.CreateModel(
            name='Rugby15s',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'male'), ('Female', 'female')], max_length=10, null=True)),
                ('age', models.CharField(blank=True, choices=[('U16', 'U16'), ('U18', 'U18'), ('U20', 'U20')], max_length=50, null=True)),
                ('participants', models.IntegerField()),
                ('number_of_groups', models.IntegerField()),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rug15champ', to='accounts.championship')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rug15season', to='dashboard.season')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rug15sport', to='accounts.sport')),
                ('teams', models.ManyToManyField(to='dashboard.schoolteam')),
            ],
        ),
        migrations.AddField(
            model_name='r15group',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r15group', to='rugby15s.rugby15s'),
        ),
        migrations.AddField(
            model_name='r15fixture',
            name='competition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rugby15s.rugby15s'),
        ),
    ]