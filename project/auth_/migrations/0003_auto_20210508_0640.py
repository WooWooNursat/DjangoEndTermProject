# Generated by Django 3.1.7 on 2021-05-08 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0002_mainuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='cvv',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='cvv'),
        ),
        migrations.AlterField(
            model_name='card',
            name='full_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='full name'),
        ),
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='number'),
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='client',
            name='card',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_.card'),
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
