# Generated by Django 2.0.5 on 2018-08-25 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photosite', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Directories',
        ),
        migrations.DeleteModel(
            name='Years',
        ),
    ]