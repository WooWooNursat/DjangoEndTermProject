from django.urls import path, include
from rest_framework import routers
from main import views

router = routers.SimpleRouter()
router.register('products', views.ProductViewSet, basename='main')
router.register('wear', views.WearViewSet, basename='main')
router.register('food', views.FoodViewSet, basename='main')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', views.category_list_view),
    path('categories/<int:id>', views.category_detailed_view),
    path('orders/', views.OrderListView.as_view()),
    path('orders/<int:id>', views.OrderDetailedView.as_view()),
    path('carts/', views.CartListView.as_view()),
    path('carts/<int:id>', views.CartDetailedView.as_view())
]
