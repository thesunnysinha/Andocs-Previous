# Generated by Django 4.0.2 on 2022-02-27 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AndocsApp', '0007_product_sub_category_alter_product_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sub_category',
        ),
    ]
