# Generated by Django 3.2 on 2021-12-27 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footballmodel', '0010_auto_20211227_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='clubPhoto',
            fields=[
                ('Club', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('club_logo_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='clubbasic',
            name='club_logo_url',
        ),
    ]
