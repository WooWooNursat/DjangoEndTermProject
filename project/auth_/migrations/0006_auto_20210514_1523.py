# Generated by Django 3.1.7 on 2021-05-14 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0005_auto_20210514_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expire_date',
            field=models.DateField(blank=True, null=True, verbose_name='expire date'),
        ),
    ]
