# Generated by Django 2.0.5 on 2018-08-25 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('photosite', '0002_auto_20180825_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('photo', models.TextField()),
            ],
        ),
    ]
