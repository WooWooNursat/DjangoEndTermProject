from django.contrib import admin
from auth_.models import MainUser, Staff, Courier, Client, Card, Profile
# Register your models here.

admin.site.register(MainUser)
admin.site.register(Staff)
admin.site.register(Courier)
admin.site.register(Client)
admin.site.register(Card)
admin.site.register(Profile)
