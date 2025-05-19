from django.db import models
from django.conf import settings
from Shop.models import Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f'{self.quantity} X {self.item}')
    
    def getTotal(self):
        total = self.item.price * self.quantity
        floatTotal = format(total, '0.2f')
        return floatTotal


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True,null=True)
    orderId = models.CharField(max_length=200,blank=True,null=True)

    def getTotals(self):
        total = 0
        for orderItem in self.orderitems.all():
            total += float(orderItem.getTotal())
        # return 
        return format(total, '0.2f')
    
    def __str__(self):
        return (f'Order Item-{self.orderitems.count()} | {self.user.email}')
    