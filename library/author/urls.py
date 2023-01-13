from django.urls import path
from .views import *


urlpatterns = [
    path('', AuthorsView.as_view(), name='authors'),
    path('create/', AddAuthor.as_view(), name='create_author'),
    path('remove/<int:pk>/', remove_author, name='remove_author'),
    path('edit/<int:pk>/', UpdateAuthor.as_view(), name='edit_author'),
]