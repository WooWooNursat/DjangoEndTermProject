# Generated by Django 3.1.7 on 2021-04-25 17:24

import auth_.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='phone number')),
                ('role', models.SmallIntegerField(choices=[(1, 'super admin'), (2, 'client'), (3, 'courier'), (4, 'staff')], default=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', auth_.models.MainUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=30, verbose_name='number')),
                ('expire_date', models.DateField(auto_now_add=True, verbose_name='expire date')),
                ('balance', models.IntegerField(default=0)),
                ('cvv', models.CharField(blank=True, max_length=3, verbose_name='cvv')),
                ('full_name', models.CharField(blank=True, max_length=30, verbose_name='full name')),
            ],
            options={
                'verbose_name': 'card',
                'verbose_name_plural': 'cards',
            },
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('mainuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth_.mainuser')),
                ('salary', models.IntegerField(default=0)),
                ('review', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'courier',
                'verbose_name_plural': 'couriers',
            },
            bases=('auth_.mainuser',),
            managers=[
                ('objects', auth_.models.MainUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('mainuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth_.mainuser')),
                ('salary', models.IntegerField(default=0, verbose_name='salary')),
            ],
            options={
                'verbose_name': 'staff',
                'verbose_name_plural': 'staff',
            },
            bases=('auth_.mainuser',),
            managers=[
                ('objects', auth_.models.MainUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '??????????????',
                'verbose_name_plural': '??????????????',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('mainuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth_.mainuser')),
                ('address', models.CharField(blank=True, max_length=30, verbose_name='address')),
                ('card', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth_.card')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
            },
            bases=('auth_.mainuser',),
            managers=[
                ('objects', auth_.models.MainUserManager()),
            ],
        ),
    ]
