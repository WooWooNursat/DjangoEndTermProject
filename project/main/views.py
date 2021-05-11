from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from main.models import Category, Product, Wear, Food, Order, Cart
from main.serializers import CategorySerializer, ShortProductSerializer, ProductSerializer, WearSerializer, \
    FoodSerializer, OrderSerializer, CartSerializer


# Create your views here.


@api_view(['GET', 'POST'])
def category_list_view(request):
    if request.method == 'GET':
        try:
            category_list = Category.objects.all()
        except:
            return JsonResponse({"404": "no category"}, safe=False)
        serializer = CategorySerializer(category_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        try:
            category = Category.objects.create(
                name=request.data.get('name')
            )
        except:
            return JsonResponse({"500": "cant create category"}, safe=False)

        return JsonResponse(CategorySerializer(category).data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detailed_view(request, id):
    if request.method == 'GET':
        try:
            category_detailed = Category.objects.get(id=id)
        except:
            return JsonResponse({"404": "no category"}, safe=False)
        serializer = CategorySerializer(category_detailed)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        try:
            category_detailed = Category.objects.get(id=id)
        except:
            return JsonResponse({"404": "no category"}, safe=False)
        category_detailed.name = request.data.get('name')
        category_detailed.save()
        serializer = CategorySerializer(category_detailed)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'DELETE':
        try:
            category_detailed = Category.objects.get(id=id)
        except:
            return JsonResponse({"404": "no category"}, safe=False)
        category_detailed.delete()
        return JsonResponse({"204": "deleted category"}, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get_serializer_class(self):
        if self.action == 'list':
            serializer_class = ShortProductSerializer
        else:
            serializer_class = ProductSerializer
        return serializer_class


class WearViewSet(viewsets.ModelViewSet):
    queryset = Wear.objects.all()
    serializer_class = WearSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartListView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDetailedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
