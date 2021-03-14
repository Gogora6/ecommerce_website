from django.db import models
from django.db.models import Sum, F
from django.utils.functional import cached_property


class Cart(models.Model):
    owner = models.OneToOneField(
        to='accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='cart'
    )

    @cached_property
    def total_cost(self):
        return self.items.aggregate(
            total_cost=Sum(F('quantity') * F('product__price'), output_field=models.CharField()))['total_cost']


class CartItem(models.Model):
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='CartItem'
    )
    cart = models.ForeignKey(
        to='cart.Cart',
        on_delete=models.CASCADE,
        related_name='items'
    )
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
