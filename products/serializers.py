import traceback

from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from .models import Category, Product, Tag


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )
        extra_kwargs = {
            'slug': {'read_only': True},
        }


class CreateProductSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('created_date', 'updated_at', 'slug')

    def create(self, validated_data):
        tags: dict = validated_data.pop('tags')
        with transaction.atomic():
            instance: Product = super().create(**validated_data)
            if type(tags) == dict and 'name' in tags.keys():
                tags_list = []
                for key in tags:
                    name = key.pop('name')
                    tags_list.append(Tag(name=name))

                tags_objects = Tag.objects.bulk_create(tags_list)
                instance.tags.set(tags_objects)
        return instance


class ProductSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('category',)
