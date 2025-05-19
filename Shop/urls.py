from django.urls import path
from Shop import views

app_name = "Shop"


urlpatterns = [
    # path('',views.test, name='test'),
    path('',views.ProductListView.as_view(), name='home'),
    path('product-detail/<pk>/',views.ProductDetail.as_view(), name='product-detail'),
]