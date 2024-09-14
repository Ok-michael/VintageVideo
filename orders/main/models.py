from django.db import models
from .managers import OrderManager

class Customer(models.Model):
    customer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Order(models.Model):
    objects = OrderManager()
    
    ORDER_STATUS = (
        (1, 'Recieved'),
        (2, 'Processing'),
        (3, 'Payment complete'),
        (4, 'Shipping'),
        (5, 'Completed'),
        (6, 'Cancelled'),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    total = models.DecimalField(
        max_digits=9, 
        decimal_places=2,
        default=0
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(
        choices=ORDER_STATUS, default='1'
    )


class Product(models.Model):
    class Meta:
        verbose_name_plural = 'Order items'
    product_id = models.IntegerField()
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )