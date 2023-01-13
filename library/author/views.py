from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator

from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import DjangoModelPermissions


class AuthorsView(LoginRequiredMixin, ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'author/authors.html'
    raise_exception = True
    #login_url = 'signin'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Authors'
        return context

    def get(self, request, *args, **kwargs):
        if request.user.role == 0:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class AddAuthor(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = AuthorForm
    template_name = 'author/create_author.html'
    success_url = reverse_lazy('authors')
    raise_exception = True
    #login_url = 'signin'
    success_message = 'Ви успішно додали автора!'

    def get(self, request, *args, **kwargs):
        if request.user.role == 0:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class UpdateAuthor(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    form_class = AuthorForm
    model = Author
    template_name = 'author/edit_author.html'
    success_url = reverse_lazy('authors')
    raise_exception = True
    # login_url = 'signin'
    success_message = 'Ви успішно оновили інформацію!'

    def get(self, request, *args, **kwargs):
        if request.user.role == 0:
            raise PermissionDenied
        id = kwargs['pk']
        if Author.get_by_id(id) is None:
            messages.error(request, 'Такого автора не існує !')
            return redirect('authors')
        return super().get(request, *args, **kwargs)


def remove_author(request, pk):
    if request.user.is_authenticated and request.user.role == 1:
        answer = Author.delete_by_id(pk)
        if answer:
            messages.success(request, "Автора було видалено")
        else:
            messages.error(request, "Виникла помилка")
        return redirect('authors')

    return HttpResponse('<h2>У дозволі відмовлено. Ваша роль має бути бібліотекарем</h2>')


#REST API
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.get_all()
    serializer_class = AuthorSerializer
    permission_classes = (DjangoModelPermissions, )