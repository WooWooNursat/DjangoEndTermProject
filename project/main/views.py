from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from auth_.models import Client
from auth_.permissions import ClientPermission, CourierPermission, StaffPermission, ClientOrAdminPermission
from utils.constants import USER_ROLE_CLIENT, USER_ROLE_COURIER
import logging

from main.models import Category, Product, Wear, Food, Order, Cart
from main.serializers import CategorySerializer, ShortProductSerializer, ProductSerializer, WearSerializer, \
    FoodSerializer, OrderSerializer, CartSerializer, GetCartSerializer, GetOrderSerializer

logger = logging.getLogger(__name__)


# Create your views here.


@api_view(['GET', 'POST'])
def category_list_view(request):
    if request.method == 'GET':
        try:
            category_list = Category.objects.all()
        except:
            logger.error(f'categories are not found')
            return JsonResponse({"404": "no category"}, safe=False)
        serializer = CategorySerializer(category_list, many=True)
        logger.info(f'categories list is returned')
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        try:
            category = Category.objects.create(
                name=request.data.get('name')
            )
        except:
            logger.error(f'category cannot be created')
            return JsonResponse({"500": "cant create category"}, safe=False)
        serializer = CategorySerializer(category)
        logger.info(f'category is created, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detailed_view(request, id):
    if request.method == 'GET':
        try:
            category_detailed = Category.objects.get(id=id)
        except:
            logger.error(f'category is not found, id: {id}')
            return JsonResponse({"404": "no category"}, safe=False)
        serializer = CategorySerializer(category_detailed)
        logger.info(f'category is returned, id: {id}')
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        try:
            category_detailed = Category.objects.get(id=id)
        except:
            logger.error(f'category is not found, id: {id}')
            return JsonResponse({"404": "no category"}, safe=False)
        category_detailed.name = request.data.get('name')
        category_detailed.save()
        serializer = CategorySerializer(category_detailed)
        logger.info(f'category is changed, id: {id}')
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'DELETE':
        try:
            category_detailed = Category.objects.get(id=id)
        except:
            logger.error(f'category is not found, id: {id}')
            return JsonResponse({"404": "no category"}, safe=False)
        category_detailed.delete()
        logger.info(f'category is deleted, id: {id}')
        return JsonResponse({"204": "deleted category"}, safe=False)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
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

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'delete':
            permission_classes = [StaffPermission, ]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'delete':
            permission_classes = [StaffPermission, ]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class OrderListView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        if self.request.user.role == USER_ROLE_CLIENT:
            orders = Order.objects.filter(client_id=self.request.user.id)
        elif self.request.user.role == USER_ROLE_COURIER:
            orders = Order.objects.filter(is_delivered=False)
        else:
            orders = Order.objects.all()
        logger.info(f'orders are returned')
        return JsonResponse(GetOrderSerializer(orders, many=True).data, safe=False)

    def post(self, request, *args, **kwargs):
        if self.request.user.role != USER_ROLE_CLIENT:
            return JsonResponse({"500": "only client can order products"}, safe=False)
        else:
            try:
                cart = Cart.objects.get(client_id=self.request.user.id)
            except:
                logger.error(f'cart is not found, user id: {id}')
                return JsonResponse({"404": "no such cart"}, safe=False)
            try:
                order = Order.objects.create(
                    client_id=self.request.user.id,
                    courier=None,
                    is_delivered=False
                )
            except:
                logger.error(f'order cannot be created')
                return JsonResponse({"500": "order cannot be created"}, safe=False)
            serializer = GetOrderSerializer(order)
            logger.info(f'order is created, id: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)


class OrderDetailedView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, id, *args, **kwargs):
        try:
            order = Order.objects.get(id=id)
        except:
            logger.error(f'order is not found, id: {id}')
            return JsonResponse({"404": "no such order"}, safe=False)
        logger.info(f'order is returned, id: {id}')
        return JsonResponse(GetOrderSerializer(order).data, safe=False)

    def put(self, request, id, *args, **kwargs):
        if self.request.user.role != USER_ROLE_COURIER:
            return JsonResponse({"500": "only courier can put data to the order"}, safe=False)
        else:
            try:
                order = Order.objects.get(id=id)
            except:
                logger.error(f'order is not found, id: {id}')
                return JsonResponse({"404": "no such order"}, safe=False)
            if self.request.data.get('is_taken'):
                order.courier_id = self.request.user.id
            if order.courier is None:
                return JsonResponse({"500": "Order cannot be delivered before the courier has taken it"})
            order.is_delivered = self.request.data.get('is_delivered')
            order.save()
            serializer = GetOrderSerializer(order)
            logger.info(f'order is changed, id: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)

    def delete(self, request, id, *args, **kwargs):
        if self.request.user.role != USER_ROLE_CLIENT:
            return JsonResponse({"500": "only client can delete the order"}, safe=False)
        else:
            try:
                order = Order.objects.get(id=id)
            except:
                logger.error(f'order is not found, id: {id}')
                return JsonResponse({"404": "no such order"}, safe=False)
            if order.client.id != self.request.user.id:
                return JsonResponse({"500": "The order belongs to another client"})
            if order.is_delivered:
                return JsonResponse({"500": "cannot be canceled because the order was delivered"})
            order.delete()
            logger.info(f'order is deleted, id: {id}')
            return JsonResponse({"204": "card has been deleted"}, safe=False)


class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]


class CartDetailedView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    permission_classes = [ClientOrAdminPermission]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCartSerializer
        elif self.request.method == 'PUT':
            return CartSerializer

    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(client=self.request.user)
        except:
            logger.error(f'cart is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such cart"}, safe=False)
        logger.info(f'cart is returned, user id: {self.request.user.id}')
        return JsonResponse(GetCartSerializer(cart).data, safe=False)

    def patch(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(client=self.request.user)
        except:
            logger.error(f'cart is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such cart"}, safe=False)
        add_products = self.request.data.get('add')
        remove_products = self.request.data.get('remove')
        if add_products is not None:
            for product in add_products:
                try:
                    cart.products.add(product)
                except:
                    logger.error(f'product is not found, id: {product}')
                    return JsonResponse({"404": "no such product"}, safe=False)
        if remove_products is not None:
            for product in remove_products:
                try:
                    cart.products.remove(product)
                except:
                    logger.error(f'product is not found, id: {product}')
                    return JsonResponse({"404": "no such product"}, safe=False)
        cart.save()
        logger.info(f'cart is changed, user id: {self.request.user.id}')
        return JsonResponse(GetCartSerializer(cart).data, safe=False)
