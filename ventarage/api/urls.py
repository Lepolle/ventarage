from django.urls import path, include
from rest_framework import routers

from .views import *
from .views import LoginView, LogoutView, SignupView


router = routers.DefaultRouter()
router.register(r'Category', CategoryView, 'category')
router.register(r'CustomProduct', CustomProductView,'product')

urlpatterns = [
    # Auth views
    path('auth/login/',
         LoginView.as_view(), name='auth_login'),
    path('auth/logout/',
         LogoutView.as_view(), name='auth_logout'),
    path('auth/signup/',
         SignupView.as_view(), name='auth_signup'),
    path('auth/reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),
    path(r'product/', CustomProductView.as_view(), name='product_list'),
    path(r'category/', CategoryView.as_view(),name='product_list_by_category'),
    path(r'product/detail/', product_detail,name='product_detail'),
]