from django.urls import path
from .views import *


urlpatterns = [
    path('', ShowOrders.as_view(), name='orders'),
    path('close/<int:pk>/', close_order, name='close_order'),
    path('open/<int:pk>/', oper_order, name='open_order'),
    path('create/', create_order, name='create_order')
]