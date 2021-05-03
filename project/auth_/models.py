from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.constants import USER_ROLES, USER_ROLE_CLIENT, USER_ROLE_STAFF, USER_ROLE_COURIER

# Create your models here.


class MainUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MainUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    phone = models.CharField(_('phone number'), max_length=30, blank=True)
    role = models.SmallIntegerField(choices=USER_ROLES, default=USER_ROLE_CLIENT)

    objects = MainUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Staff(MainUser):
    salary = models.IntegerField(_('salary'), default=0)
    role = USER_ROLE_STAFF
    is_staff = True

    class Meta:
        verbose_name = _('staff')
        verbose_name_plural = _('staff')


class Courier(MainUser):
    salary = models.IntegerField(default=0)
    review = models.FloatField(default=0)
    role = USER_ROLE_COURIER
    is_staff = False

    class Meta:
        verbose_name = _('courier')
        verbose_name_plural = _('couriers')


class Card(models.Model):
    number = models.CharField(_('number'), max_length=30, blank=True)
    expire_date = models.DateField(_('expire date'), auto_now_add=True)
    balance = models.IntegerField(default=0)
    cvv = models.CharField('cvv', max_length=3, blank=True)
    full_name = models.CharField(_('full name'), max_length=30, blank=True)

    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')

    def __str__(self):
        return self.number


class ClientManager(MainUserManager):
    def get_client_card(self):
        return self.get_related().card

    def get_related(self):
        return self.select_related('card')


class Client(MainUser):
    address = models.CharField(_('address'), max_length=30, blank=True)
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    role = USER_ROLE_CLIENT
    is_staff = False

    objects = ClientManager

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')


class Profile(models.Model):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

