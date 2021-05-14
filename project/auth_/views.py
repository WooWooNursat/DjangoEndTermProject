from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from auth_.permissions import ClientPermission
from auth_ import models, serializers
import logging

logger = logging.getLogger(__name__)


# Create your views here.


class ClientViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [ClientPermission]
        return [permission() for permission in permission_classes]

    def create(self, request):
        try:
            user = models.Client.objects.create_user(
                email=self.request.data.get('email'),
                password=self.request.data.get('password'),
                phone=self.request.data.get('phone'),
                address=self.request.data.get('address')
            )
        except ValueError as e:
            logger.error(f'client cannot be created, error: {e}')
            return JsonResponse({"500": e}, safe=False)
        serializer = serializers.ClientSerializer(user)
        logger.info(f'client is created, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request):
        try:
            user = models.Client.objects.get(id=self.request.user.id)
        except:
            logger.error(f'client is not found, id: {self.request.user.id}')
            return JsonResponse({"404": "no such user"})
        serializer = serializers.ClientSerializer(user)
        logger.info(f'client is returned, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)

    def update(self, request):
        try:
            user = models.Client.objects.get(id=self.request.user.id)
        except:
            logger.error(f'client is not found, id: {self.request.user.id}')
            return JsonResponse({"404": "no such user"})
        user.phone = self.request.data.get('phone')
        user.address = self.request.data.get('address')
        user.save()
        serializer = serializers.ClientSerializer(user)
        logger.info(f'client is updated, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)


class StaffViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser, ]

    def create(self, request):
        try:
            user = models.Staff.objects.create_user(
                email=self.request.data.get('email'),
                password=self.request.data.get('password'),
                phone=self.request.data.get('phone'),
                salary=self.request.data.get('salary')
            )
        except ValueError as e:
            logger.error(f'staff cannot be created, error: {e}')
            return JsonResponse({"500": e}, safe=False)
        serializer = serializers.StaffSerializer(user)
        logger.info(f'staff is created, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)


class CourierViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser, ]

    def create(self, request):
        try:
            user = models.Courier.objects.create_user(
                email=self.request.data.get('email'),
                password=self.request.data.get('password'),
                phone=self.request.data.get('phone'),
                salary=self.request.data.get('salary')
            )
        except ValueError as e:
            logger.error(f'courier cannot be created, error: {e}')
            return JsonResponse({"500": e}, safe=False)
        serializer = serializers.CourierSerializer(user)
        logger.info(f'courier is created, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)


class ProfileViewSet(viewsets.ViewSet):
    def update(self, request):
        try:
            profile = models.Profile.objects.get(user=self.request.user)
        except:
            logger.error(f'profile is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such profile"})
        profile.bio = self.request.data.get('bio')
        profile.birth_date = self.request.data.get('birth_date')
        profile.save()
        serializer = serializers.ProfileSerializer(profile)
        logger.info(f'profile is updated, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request):
        try:
            profile = models.Profile.objects.get(user=self.request.user)
        except:
            logger.error(f'profile is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such profile"})
        serializer = serializers.ProfileSerializer(profile)
        logger.info(f'profile is returned, id: {serializer.instance}')
        return JsonResponse(serializer.data, safe=False)


class CardViewSet(viewsets.ViewSet):
    permission_classes = [ClientPermission, ]

    def update(self, request):
        try:
            client = models.Client.objects.get(id=self.request.user.id)
        except:
            logger.error(f'client is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such client"})
        try:
            card = models.Card.objects.get(id=client.card.id)
        except:
            logger.error(f'card is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such card"})
        card.number = self.request.data.get('number')
        card.full_name = self.request.data.get('full_name')
        card.expire_date = self.request.data.get('expire_date')
        card.cvv = self.request.data.get('cvv')
        balance = self.request.data.get('balance')
        if balance is not None:
            card.balance = balance
        card.save()
        logger.info(f'card is updated, user id: {self.request.user.id}')
        return JsonResponse({"200": "card info has changed"})

    def retrieve(self, request):
        try:
            client = models.Client.objects.get(id=self.request.user.id)
        except:
            logger.error(f'client is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such client"})
        try:
            card = models.Card.objects.get(id=client.card.id)
        except:
            logger.error(f'card is not found, user id: {self.request.user.id}')
            return JsonResponse({"404": "no such card"})
        serializer = serializers.CardSerializer(card)
        logger.info(f'card is returned, user id: {self.request.user.id}')
        return JsonResponse(serializer.data, safe=False)
