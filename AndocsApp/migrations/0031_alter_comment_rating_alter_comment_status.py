# Generated by Django 4.0.3 on 2022-10-11 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AndocsApp', '0030_alter_comment_rating_alter_comment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(choices=[('4', '4'), ('3', '3'), ('5', '5'), ('2', '2'), ('1', '1')], default='1'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('False', 'False'), ('True', 'True'), ('New', 'New')], default='New', max_length=10),
        ),
    ]