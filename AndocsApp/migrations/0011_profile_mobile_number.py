# Generated by Django 4.0.2 on 2022-02-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AndocsApp', '0010_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobile_number',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
