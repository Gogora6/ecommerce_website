from django.utils.translation import ugettext_lazy as _
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    expiration_date = models.DateTimeField(verbose_name=_('Coupon Expiration Date'))
    discount = models.IntegerField(verbose_name=_('Discount'), help_text='%')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')


class Order(models.Model):
    products = models.ManyToManyField(to='products.Product', related_name='orders')
    coupon = models.ForeignKey(
        to='orders.Coupon', related_name='orders',
        on_delete=models.PROTECT,
        null=True, blank=True,
    )
    user = models.ForeignKey(
        to='accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
