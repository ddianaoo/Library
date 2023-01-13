from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import ROLE_CHOICES

from rest_framework import viewsets, views
from .serializers import CustomUserSerializer, LoginSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import CreateAPIView

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from .signin import EmailAuthBackend
from .permissions import *


def create(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # только регистрация
            form.save()
            messages.success(request, 'Успішна регістрація!')
            return redirect('signin')

            # регистрация и вход
            # user = form.save()
            # login(request, user, backend='authentication.signin.EmailAuthBackend')
            # messages.success(request, 'Успішна регістрація! Ви увійшли!')
            # return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'authentication/create.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='authentication.signin.EmailAuthBackend')
            messages.success(request, 'Ви увійшли')
            return redirect('home')
        else:
            error = {}
            for field in form.errors:
                error[field] = form.errors[field].as_text()
            messages.error(request, *[e[1:] for e in error.values()])
            form = UserLoginForm()
    else:
        form = UserLoginForm()
    return render(request, 'authentication/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


# librarian/
class UserList(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'authentication/get_list.html'
    raise_exception = True
    context_object_name = 'users'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        if request.user.role == 0:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        users = CustomUser.get_all()
        context['users_lenght'] = len(users)
        context['title'] = 'List of users'
        return context


def get_user(request, email):
    if request.user.is_authenticated and request.user.role == 1:
        user = CustomUser.get_by_email(email)
        context = {'user': user, 'title': 'Get data by User'}
        return render(request, 'authentication/single_user.html', context)
    return HttpResponse('<h2>У дозволі відмовлено. Ваша роль має бути бібліотекарем</h2>')


def edit(request):
    user_id = request.user.id
    user = CustomUser.get_by_id(user_id)
    if user is None:
        messages.error(request, 'Спочатку треба увійти/зареєструватися !')
        return redirect('home')
    if user.id != request.user.id:
        return HttpResponse('Ви не можете змінювати усі інші аккаунти, крім свого')

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успішне редагування! Зайдіть знов!')
            return redirect('home')
        else:
            messages.error(request, form.errors)
            form = UserUpdateForm(instance=request.user)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'authentication/edit.html', {'form': form})


# REST API
class CustomUserViewSet(viewsets.ModelViewSet):
    # queryset = CustomUser.get_all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list':
            self.permission_classes = [IsSuperUserOrNotAuthenticate, ]
        elif self.request.user.is_authenticated:
            if self.action == 'list':
                self.permission_classes = [IsAdminUser, ]

            if self.action == 'retrieve':
                self.permission_classes = [IsOwnerOrStaff, ]

            if self.action == 'update':
                self.permission_classes = [IsOwnerOrSuperUser, ]

            if self.action == 'destroy':
                self.permission_classes = [IsOwnerOrSuperUser, ]
        else:
            self.permission_classes = [IsNotAllowed, ]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CustomUser.objects.all()
        return []


class AuthenticatedView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        msg = {
            'message': f'Hi {request.user.email}! Your role is {ROLE_CHOICES[request.user.role][1]} ! Congratulations on being authenticated!'}
        return Response(msg, status=status.HTTP_200_OK)
