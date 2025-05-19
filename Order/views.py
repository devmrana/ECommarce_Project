from django.shortcuts import render,get_object_or_404, redirect

# Authentication
from django.contrib.auth.decorators import login_required

# Models
from Order.models import Cart,Order
from Shop.models import Product
# Messages
from django.contrib import messages
# Create your views here.

@login_required
def addToCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    # print("Item")
    # print(item)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    # print("Order Item Object:")
    # print(order_item)
    # print(order_item[0])
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # print("Order Qs:")
    # print(order_qs)
    #print(order_qs[0])
    if order_qs.exists():
        order = order_qs[0]
        # print("If Order exist")
        # print(order)
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated.")
            return redirect("Shop:home")
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("Shop:home")
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item was added to your cart.")
        return redirect("Shop:home")

@login_required
def cartView(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)
    orders = Order.objects.filter(user=request.user, ordered = False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'Order/cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(request,"You don't have any item in your cart!")
        return redirect("Shop:home")
    
@login_required
def removeItemCart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user,purchased=False)[0]
            # order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.info(request,"This item was remove  your cart!")
            return redirect("Order:cart")
        else:
            messages.info(request,"This item was not in your cart!")
            return redirect("Shop:home")
    else:
        messages.info(request,"You don't have an active item!")
        return redirect("Shop:home")


@login_required
def increaseCartItem(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                return redirect("Order:cart")
        else:
            messages.warning(request,f"{item.name} is not in your cart!")
            return redirect("Order:cart")
    else:
        messages.info(request,"You don't have an active order!")
        return redirect("Shop:home")


@login_required
def decreaseCartItem(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                return redirect("Order:cart")
            else:
                return redirect("Order:cart")
        else:
            messages.warning(request,f"{item.name} is not in your cart!")
            return redirect("Order:cart")
    else:
        messages.info(request,"You don't have an active order!")
        return redirect("Shop:home")






