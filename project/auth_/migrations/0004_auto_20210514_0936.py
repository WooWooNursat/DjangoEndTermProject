# Generated by Django 3.1.7 on 2021-05-14 09:36

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0003_auto_20210508_0640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AlterField(
            model_name='card',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='card',
            name='cvv',
            field=models.CharField(blank=True, max_length=3, null=True, validators=[utils.validators.validate_card_cvv], verbose_name='cvv'),
        ),
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[utils.validators.validate_card_number], verbose_name='number'),
        ),
        migrations.AlterField(
            model_name='courier',
            name='review',
            field=models.PositiveIntegerField(default=0, validators=[utils.validators.validate_review]),
        ),
        migrations.AlterField(
            model_name='courier',
            name='salary',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[utils.validators.validate_phone_number], verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='salary',
            field=models.PositiveIntegerField(default=0, verbose_name='salary'),
        ),
    ]
