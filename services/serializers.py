from rest_framework import serializers
from .models import Category, Service
from users.models import User


class ServiceSerializer(serializers.ModelSerializer):
    provider = serializers.ReadOnlyField(source='provider.username')
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "provider",
            "name",
            "slug",
            "description",
            "price",
            "category",
            "category_name",
            "city",
            "available_dates",
            "rating",
            "image",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["provider", "rating", "created_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "parent"]