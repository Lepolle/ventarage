from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    email = serializers.EmailField(
        required=True)
    password = serializers.CharField(
        min_length=8)

    def validate_password(self, value):
        return make_password(value)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class CustomProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomProduct
        fields = ('category', 'name', 'slug', 'image', 'description', 'price', 'available',
                  'created', 'updated')