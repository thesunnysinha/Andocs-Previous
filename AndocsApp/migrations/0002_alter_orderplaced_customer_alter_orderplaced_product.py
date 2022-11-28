# Generated by Django 4.0.2 on 2022-02-25 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AndocsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AndocsApp.customer'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AndocsApp.product'),
        ),
    ]