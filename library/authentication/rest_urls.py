from django.urls import path, include
from rest_framework import routers
from .views import *
from order.views import OrderByUserViewSet

router = routers.DefaultRouter()
router.register('', CustomUserViewSet, basename='CustomUser')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:user_id>/order/', OrderByUserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:user_id>/order/<int:pk>/', OrderByUserViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
]