# Generated by Django 3.2 on 2021-12-25 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footballmodel', '0007_clubbasic_clubphoto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubbasic',
            name='id',
        ),
        migrations.RemoveField(
            model_name='clubphoto',
            name='id',
        ),
        migrations.AlterField(
            model_name='clubbasic',
            name='Club',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='clubphoto',
            name='Club',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
