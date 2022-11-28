# Generated by Django 4.0.3 on 2022-11-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AndocsApp', '0037_profile_birth_date_profile_profile_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(choices=[(5, '5'), (3, '3'), (2, '2'), (1, '1'), (4, '4')], default='1'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('True', 'True'), ('False', 'False')], default='New', max_length=10),
        ),
    ]