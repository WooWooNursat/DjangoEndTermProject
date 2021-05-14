# Generated by Django 3.1.7 on 2021-05-14 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0006_auto_20210514_1523'),
        ('main', '0004_auto_20210514_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_.client', verbose_name='client'),
        ),
        migrations.AlterField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_.courier', verbose_name='courier'),
        ),
    ]
