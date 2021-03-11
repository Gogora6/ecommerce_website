from django.contrib import admin

# Register your models here.

from .models import Tag


@admin.register(Tag)
class CarTypeAdmin(admin.ModelAdmin):
    pass
