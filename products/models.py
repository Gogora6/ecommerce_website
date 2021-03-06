from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.db import models


class Category(models.Model):
    # @TODO add a subcategory
    name = models.CharField(max_length=50, verbose_name=_('Category Name'))
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    order = models.PositiveSmallIntegerField(verbose_name=_('Order'), blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        to='products.Category',
        on_delete=models.PROTECT,
        related_name='products'
    )
    tags = models.ManyToManyField(
        to='products.Tag',
        related_name='product'
    )
    title = models.CharField(max_length=100, verbose_name=_('Product Title'))
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    brand = models.CharField(max_length=50, verbose_name=_('Brand Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Product Description'))
    ingredients = models.TextField(null=True, blank=True, verbose_name=_('Product Ingredients'))

    UPC = models.CharField(null=True, blank=True, verbose_name=_('Product UPC'), max_length=12)
    SKU = models.CharField(null=True, blank=True, verbose_name=_('Product SKU'), max_length=10)

    image = models.ImageField(verbose_name=_("Image"), upload_to='products', blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    stocks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Tag'))

    def __str__(self):
        return self.name
