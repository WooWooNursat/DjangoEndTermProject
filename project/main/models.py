from django.db import models
from django.utils.translation import ugettext_lazy as _
from auth_.models import Client, Courier
# Create your models here.


class Category(models.Model):
    name = models.CharField(_('name'), max_length=30, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_category(self):
        return self.get_related().category

    def get_related(self):
        return self.select_related('category')


class ProductAbstract(models.Model):
    name = models.CharField(_('name'), max_length=30, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    price = models.IntegerField(_('price'), default=0)
    # image = models.ImageField(_('image'), )
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_('category'))

    objects = ProductManager

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Product(ProductAbstract):
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Wear(Product):
    size = models.CharField(_('size'), max_length=10, blank=True)
    materials = models.TextField(_('materials'), null=True, blank=True)

    class Meta:
        verbose_name = 'wear'
        verbose_name_plural = 'wear'

    def __str__(self):
        return self.name


class Food(Product):
    ingredients = models.TextField(_('ingredients'), null=True, blank=True)

    class Meta:
        verbose_name = 'food'
        verbose_name_plural = 'food'

    def __str__(self):
        return self.name


class OrderManager(models.Manager):
    def get_order_client(self):
        return self.get_related().client

    def get_order_courier(self):
        return self.get_related().courier

    def get_related(self):
        return self.select_related('client', 'courier')


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_('client'))
    courier = models.ForeignKey(Courier, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_('courier'))
    is_delivered = models.BooleanField(default=False)

    objects = OrderManager

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.id


class CartManager(models.Manager):
    def get_order(self):
        return self.get_related().order

    def get_related(self):
        return self.select_related('order')


class Cart(models.Model):
    products = models.ManyToManyField(Product)
    amount = models.IntegerField(_('amount'), default=1)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_('order'))

    objects = CartManager

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return self.id
