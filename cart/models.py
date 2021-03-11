from django.db import models


class Cart(models.Model):
    owner = models.OneToOneField(
        to='accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='cart'
    )


class CartItem(models.Model):
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='CartItem'
    )
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
    cart = models.ForeignKey(
        to='cart.Cart',
        on_delete=models.CASCADE,
        related_name='items'
    )
