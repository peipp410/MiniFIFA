# Generated by Django 3.2 on 2021-12-25 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footballmodel', '0003_auto_20211223_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='playerDisplay',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Crossing', models.IntegerField()),
                ('Finishing', models.IntegerField()),
                ('HeadingAccuracy', models.IntegerField()),
                ('ShortPassing', models.IntegerField()),
                ('Volleys', models.IntegerField()),
                ('Dribbling', models.IntegerField()),
                ('Curve', models.IntegerField()),
                ('FKAccuracy', models.IntegerField()),
                ('LongPassing', models.IntegerField()),
                ('BallControl', models.IntegerField()),
                ('Acceleration', models.IntegerField()),
                ('SprintSpeed', models.IntegerField()),
                ('Agility', models.IntegerField()),
                ('Reactions', models.IntegerField()),
                ('Balance', models.IntegerField()),
                ('ShotPower', models.IntegerField()),
                ('Jumping', models.IntegerField()),
                ('Stamina', models.IntegerField()),
                ('Strength', models.IntegerField()),
                ('LongShots', models.IntegerField()),
                ('Aggression', models.IntegerField()),
                ('Interceptions', models.IntegerField()),
                ('Positioning', models.IntegerField()),
                ('Vision', models.IntegerField()),
                ('Penalties', models.IntegerField()),
                ('Composure', models.IntegerField()),
                ('Marking', models.IntegerField()),
                ('StandingTackle', models.IntegerField()),
                ('SlidingTackle', models.IntegerField()),
                ('GKDiving', models.IntegerField()),
                ('GKHandling', models.IntegerField()),
                ('GKKicking', models.IntegerField()),
                ('GKPositioning', models.IntegerField()),
                ('GKReflexes', models.IntegerField()),
            ],
        ),
    ]
