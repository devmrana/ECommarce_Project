from django.urls import path
from Order import views

app_name = "Order"

urlpatterns = [
    path('add/<pk>/', views.addToCart,name='add'),
    path('cart/',views.cartView, name='cart'),
    path('remove/<pk>',views.removeItemCart, name='remove'),
    path('increase/<pk>',views.increaseCartItem, name='increase'),
    path('decrease/<pk>',views.decreaseCartItem, name='decrease'),
]