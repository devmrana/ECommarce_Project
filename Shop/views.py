from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from Shop.models import Product
# Create views here.
# def test(request):
#     return render(request, 'shop/index.html')

class ProductListView(ListView):
    model = Product
    template_name = "Shop/home.html"


from django.contrib.auth.mixins import LoginRequiredMixin
class ProductDetail(DetailView,LoginRequiredMixin):
    model = Product
    template_name = 'Shop/product_detail.html'
    context_object_name = 'productdetail'