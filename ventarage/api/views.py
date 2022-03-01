from django.contrib.auth import authenticate, login, logout
from django.dispatch import receiver
from django.shortcuts import render
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, CustomProduct
from .serializers import *


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email,username=username, password=password)

        if user:
            login(request, user)
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK)

        return Response(
            status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    def post(self, request):
        logout(request)

        return Response(status=status.HTTP_200_OK)


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(
        f"\nRecupera la contraseña del correo '{reset_password_token.user.email}' usando el token '{reset_password_token.key}' desde la API http://localhost:8000/api/auth/reset/confirm/.")


class CategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CustomProductView(generics.CreateAPIView):
    serializer_class = CustomProductSerializer
    queryset = CustomProduct.objects.all()


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = CustomProduct.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'product/list.html',
                  {'category': category, 'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(CustomProduct, id=id, slug=slug, available=True)
    return render(request, 'header.html', {'product': product})