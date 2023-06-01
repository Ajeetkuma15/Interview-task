from .views import *
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/shoplocation_list/', shoplocation_list, name='shoplocation_list'),
    path('api/shop_details/<int:pk>/', shop_details, name='shop_details'),
]