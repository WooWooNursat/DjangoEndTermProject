from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from auth_ import views

urlpatterns = [
    path('', obtain_jwt_token),
    path('clients/', views.ClientViewSet.as_view({'post': 'create', 'get': 'retrieve', 'put': 'update'})),
    path('staff/', views.StaffViewSet.as_view({'post': 'create'})),
    path('couriers/', views.CourierViewSet.as_view({'post': 'create'})),
    path('profile/', views.ProfileViewSet.as_view({'put': 'update', 'get': 'retrieve'})),
    path('card/', views.CardViewSet.as_view({'put': 'update', 'get': 'retrieve'}))
]
