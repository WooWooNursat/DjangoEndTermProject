from rest_framework import serializers
from main.models import Category, Product, Wear, Food, Order, Cart
from auth_.serializers import ClientSerializer, CourierSerializer, StaffSerializer


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)


class ShortProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image')


class ProductSerializer(ShortProductSerializer):
    class Meta(ShortProductSerializer.Meta):
        model = Product
        fields = ShortProductSerializer.Meta.fields + ('description', 'category')


class WearSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        model = Wear
        fields = ProductSerializer.Meta.fields + ('size', 'materials')


class FoodSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        model = Food
        fields = ProductSerializer.Meta.fields + ('ingredients',)


class GetOrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    courier = CourierSerializer()
    products = ProductSerializer(many=True)
    # is_delivered = serializers.BooleanField()

    class Meta:
        model = Order
        fields = ('client', 'courier', 'products', 'is_delivered')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('client', 'courier', 'products', 'is_delivered')


class CartSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Cart
        fields = ('products', 'client',)


class GetCartSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('products', 'client')
