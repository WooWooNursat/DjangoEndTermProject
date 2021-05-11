from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from auth_.permissions import ClientPermission
from auth_ import models, serializers


# Create your views here.


class ClientViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [ClientPermission, ]
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
            return JsonResponse({"500": e}, safe=False)
        serializer = serializers.ClientSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request):
        try:
            user = models.Client.objects.get(id=self.request.user.id)
        except:
            return JsonResponse({"404": "no such user"})
        serializer = serializers.ClientSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    def update(self, request):
        try:
            user = models.Client.objects.get(id=self.request.user.id)
        except:
            return JsonResponse({"404": "no such user"})
        user.phone = self.request.data.get('phone')
        user.address = self.request.data.get('address')
        user.save()
        serializer = serializers.ClientSerializer(user)
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
            return JsonResponse({"500": e}, safe=False)
        serializer = serializers.StaffSerializer(user)
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
            return JsonResponse({"500": e}, safe=False)
        serializer = serializers.CourierSerializer(user)
        return JsonResponse(serializer.data, safe=False)


class ProfileViewSet(viewsets.ViewSet):
    def update(self, request):
        try:
            profile = models.Profile.objects.get(user=self.request.user)
        except:
            return JsonResponse({"404": "no such profile"})
        profile.bio = self.request.data.get('bio')
        profile.birth_date = self.request.data.get('birth_date')
        profile.save()
        serializer = serializers.ProfileSerializer(profile)
        return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request):
        try:
            profile = models.Profile.objects.get(user=self.request.user)
        except:
            return JsonResponse({"404": "no such profile"})
        serializer = serializers.ProfileSerializer(profile)
        return JsonResponse(serializer.data, safe=False)


class CardViewSet(viewsets.ViewSet):
    permission_classes = [ClientPermission, ]

    def update(self, request):
        try:
            card = models.Card.objects.get(id=self.request.user.card.id)
        except:
            return JsonResponse({"404": "no such card"})
        card.number = self.request.data.get('number')
        card.full_name = self.request.data.get('full_name')
        card.expire_date = self.request.data.get('expire_date')
        card.cvv = self.request.data.get('cvv')
        card.balance = self.request.data.get('balance')
        card.save()
        return JsonResponse({"200": "card info has changed"})

    def retrieve(self, request):
        try:
            card = models.Card.objects.get(id=self.request.user.card.id)
        except:
            return JsonResponse({"404": "no such card"})
        serializer = serializers.CardSerializer(card)
        return JsonResponse(serializer.data, safe=False)
