from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import View
import sys
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets

from author.models import Author
from .models import Book
from django.db.models import Q
from django.shortcuts import render
from order.models import Order
from authentication.models import CustomUser
from .forms import CreateBookForm, UpdateBookForm, UserBooksForm, FilterBooksForm
from django.views.generic import ListView
from .serializers import BookSerializer

from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class BooksViewBase(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'book/base.html'
    paginate_by = 6


class BooksView(View):
    model = Book
    template_name = 'book/books.html'
    filter_form = FilterBooksForm

    def get_context(self):
        context = {'authors': Author.objects.all()}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        context['form'] = self.filter_form()
        context['books'] = Book.objects.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post_data = dict(**self.request.POST)
        book_ids = [int(i) for i in post_data.get('books', [])]
        author_ids = [int(i) for i in post_data.get('authors', [])]
        context = self.get_context()
        context['books'] = Book.objects.filter(Q(pk__in=book_ids) | Q(authors__in=author_ids)).distinct()
        context['form'] = FilterBooksForm(post_data)
        return render(request, self.template_name, context)


class BookView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book/book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = context['book'].authors.all()

        return context


class FilteredBooksView(ListView):
    model = Book
    template_name = 'book/books.html'
    context_object_name = 'books'

    def get_queryset(self):
        post_data = self.request.POST
        return Book.objects.filter(Q(name__in=post_data["book"]) | Q(authors__in=post_data["author"]))

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex["authors"] = Author.objects.all()
        # print(contex["authors"])
        return contex


def get_user_books(request):
    users = CustomUser.objects.filter(role=0)
    form = UserBooksForm()
    if request.user.role == 1:
        if request.method == "POST":
            pk = request.POST['user']
            orders = Order.objects.filter(user_id=pk)
            user = CustomUser.objects.get(pk=pk)
            length = len(orders)
            return render(request, 'book/user_books.html', context={'orders': orders,
                                                                    'user': user,
                                                                    'users': users,
                                                                    'length': length,
                                                                    'form': form, })

        return render(request, 'book/user_books.html', context={'orders': None,
                                                                'user': None,
                                                                'users': users,
                                                                'form': form, })
    raise PermissionDenied


class CreateBookView(LoginRequiredMixin, FormView):
    form_class = CreateBookForm
    template_name = 'book/create_book.html'

    def form_valid(self, form):
        Book.create(**form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('base')

    def get(self, request, *args, **kwargs):
        if request.user.role == 0:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class UpdateBookView(LoginRequiredMixin, FormView):
    form_class = UpdateBookForm
    template_name = 'book/update_book.html'

    def form_valid(self, form):
        book = Book.get_by_id(self.kwargs['pk'])
        book.update(**form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books')

    def get_context_data(self, **kwargs):
        obj = Book.get_by_id(self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['form'] = self.form_class(obj.__dict__)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.role == 0:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


def delete_book(request, pk):
    if request.user.role == 1:
        Book.delete_by_id(pk)
        return redirect('books')
    raise PermissionDenied


# REST API
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )