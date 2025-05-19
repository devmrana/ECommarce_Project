from django.shortcuts import render, HttpResponseRedirect,redirect
from django.contrib import messages
# Models and Forms
from Order.models import Order, Cart
from Payment.forms import BillingForm
# from .forms import *
from Payment.models import BillingAddress
from django.contrib.auth.decorators import login_required
from num2words import num2words

# For Payment
# import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# For View
@login_required
def checkOut(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    print(saved_address)
    saved_address = saved_address[0]
    print(saved_address)
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, 'Address Updated successfully..!')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    print(order_items)
    order_total = order_qs[0].getTotals()
    number_to_words = num2words(order_total)
    print(order_total)
    return render(request, 'Payment/checkout.html',context={'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address,'number_to_words':number_to_words})



# Payment View
@login_required
def payment(request):
    save_address = BillingAddress.objects.get_or_create(user=request.user)
    save_address = save_address[0]
    if not save_address.is_fully_filled():
        messages.info(request,'Please complete shipping addrss!')
        return redirect("Payment:checkout")
    if not request.user.profile.is_fully_filled():
        messages.info(request,'Please complete profile details!')
        return redirect("LoginApp:changeprofile")

    store_id = 'minis63fe00f51aa1a'
    api_key = 'minis63fe00f51aa1a@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=api_key)
    status_url = request.build_absolute_uri(reverse("Payment:complete"))
    print(status_url)
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].getTotals()

    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='clothing', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')

    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=save_address.address, city=save_address.city, postcode=save_address.zipcode, country=save_address.country)

    response_data = mypayment.init_payment()
    # print(response_data)
    return redirect(response_data['GatewayPageURL'])
    # return render(request,'Payment/payment.html',context={})

@csrf_exempt
def complete(request):
    if request.method =='POST' or request.method =='post':
        payment_data = request.POST
        # print(payment_data)
        
        status = payment_data['status']
        if status == 'VALID':
            card_type = payment_data['card_type']
            card_brand = payment_data['card_brand']
            amount = payment_data['amount']
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            bank_tran_id = payment_data['bank_tran_id']
            messages.success(request,f'Payment successfully!')
            return HttpResponseRedirect(reverse('Payment:purchase',kwargs={'val_id':val_id,'tran_id':tran_id}))
        elif status == 'FAILED':
            messages.warning(request,f'Payment Failed!')
        elif status == 'CANCELLED':
            messages.warning(request,f'Payment cancle, Try again!')
            return HttpResponseRedirect(reverse('Order:cart'))
        # else:
        #     messages.info(request,f'Payment successfully, But Risk!')
    return render(request,'Payment/complete.html',context={'status':status})

@login_required
def purchased(request,val_id,tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()
    cart_item = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_item:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('Shop:home'))

@login_required
def orderView(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True).order_by('-created')
        context = {'orders':orders}
    except:
        messages.warning(request, 'You do not have an active order')
        return redirect('Shopp:home')
    return render(request, "Payment/order.html", context)