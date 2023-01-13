from django.urls import path
from .views import *


urlpatterns = [
    path('', BooksViewBase.as_view(), name='base'),
    path('filter/', BooksView.as_view(), name='books'),
    path('<int:pk>/', BookView.as_view(), name='book'),
    path('filter/user/', get_user_books, name="user_books"),
    path('create_book/', CreateBookView.as_view(), name='create_book'),
    path('update_book/<int:pk>/', UpdateBookView.as_view(), name='update_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
]