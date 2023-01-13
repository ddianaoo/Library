from django.urls import path
from .views import *


urlpatterns = [
    path('create/', create, name='create'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('edit/', edit, name='edit'),
    path('user/<str:email>/', get_user, name='get_user'),
    path('users/', UserList.as_view(), name='list_users'),
]