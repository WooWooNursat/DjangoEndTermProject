from rest_framework import serializers
from main.models import Category, Product, Wear, Food, Order, Cart
from auth_.serializers import ClientSerializer, CourierSerializer, StaffSerializer


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)


class ShortProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image')


class ProductSerializer(ShortProductSerializer):
    category = CategorySerializer()

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


class OrderSerializer(serializers.Serializer):
    client = ClientSerializer()
    courier = CourierSerializer()
    is_delivered = serializers.BooleanField()


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    order = OrderSerializer()

    class Meta:
        model = Cart
        fields = ('products', 'amount', 'order',)
