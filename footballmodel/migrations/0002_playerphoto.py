# Generated by Django 3.2 on 2021-12-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footballmodel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='playerPhoto',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('PhotoUrl', models.CharField(max_length=255)),
            ],
        ),
    ]
