from django.urls import path
from Payment import views
app_name = "Payment"

urlpatterns = [
    path('checkout/',views.checkOut, name='checkout'),
    path('pay/',views.payment, name='pay'),
    path('status/',views.complete, name='complete'),
    path('purchased/<val_id>/<tran_id>/',views.purchased,name='purchase'),
    path('orders/', views.orderView, name='orders'),
]
