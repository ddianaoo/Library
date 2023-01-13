from django.views.generic import ListView, DetailView
from rest_framework import viewsets

from .models import *
from datetime import datetime as dt, timedelta
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from book.models import Book
from authentication.models import CustomUser
from django.core.paginator import Paginator
from .forms import CreateOrderForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from .serializers import OrderSerializer
from .permissions import NotAllowedUpdateAndDeletePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


class ShowOrders(LoginRequiredMixin, ListView):
    template_name = 'order/orders.html'
    context_object_name = 'orders'
    paginate_by = 3
    raise_exception = True

    def get_queryset(self):
        user = self.request.user
        if self.request.user.role == 0:
            res = Order.objects.filter(user_id=user.pk)
        else:
            res = Order.objects.all()
        return res

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.id)
        return context


def close_order(request, pk):
    if request.user.is_authenticated and request.user.role == 1:
        order = Order.objects.get(pk=pk)
        order.end_at = dt.now()
        order.save()
        return redirect('orders')
    raise PermissionDenied


def oper_order(request, pk):
    if request.user.is_authenticated and request.user.role == 1:
        order = Order.objects.get(pk=pk)
        order.end_at = None
        order.save()
        return redirect('orders')
    raise PermissionDenied


def create_order(request):
    if request.user.is_authenticated and request.user.role == 0:
        if request.method == 'POST':
            try:
                book = Book.objects.get(pk=request.POST['book'])
                user = CustomUser.objects.get(pk=request.user.pk)
                plated_end_at = dt.now() + timedelta(days=14)
                order = Order.create(user, book, plated_end_at)
                if not order:
                    raise ValueError
            except:
                messages.error(request, "Введені некоректні дані або книги закінчились")
            else:
                messages.success(request, 'Книга успішно замовлена')
                return redirect('orders')

        return render(request, 'order/create_order.html', context={'books': Book.objects.all(),
                                                                   'form': CreateOrderForm()})
    raise PermissionDenied


# REST API
class OrderViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (NotAllowedUpdateAndDeletePermission, )

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role != 0:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user.pk)




class OrderByUserViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (NotAllowedUpdateAndDeletePermission, )

    def get_user_id(self):
        user_id = self.request.META['PATH_INFO'].split('/')[4]
        return user_id

    def get_queryset(self):
        user_id = self.get_user_id()
        return Order.get_by_user(user_id)

    def create(self, request, user_id):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user_creation_id = serializer.validated_data['user'].id
            if user_creation_id == user_id:
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(f'Ви намагаєтесь присвоїти замовлення іншому замовнику, спробуйте ще раз з id = {user_id}', status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # def get_serializer_class(self):
    #     serializer_class = self.serializer_class
    #     if self.request.method == 'POST':
    #         serializer_class = OrderSerializer2
    #     return serializer_class

