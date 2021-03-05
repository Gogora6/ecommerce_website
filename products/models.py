from django.utils.translation import ugettext_lazy as _
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Product Title'))
    slug = models.CharField(max_length=150, verbose_name=_('Product slug'))
    brand = models.CharField(max_length=50, verbose_name=_('Brand Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Product Description'))
    ingredients = models.TextField(null=True, blank=True, verbose_name=_('Product Ingredients'))

    UPC = models.CharField(null=True, blank=True, verbose_name=_('Product UPC'), max_length=12)
    SKU = models.CharField(null=True, blank=True, verbose_name=_('Product SKU'), max_length=10)

    image = models.ImageField(verbose_name=_("Image"), upload_to='profiles', blank=True, null=True)

    price = models.IntegerField()
    stocks = models.IntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title