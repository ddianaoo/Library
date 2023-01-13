"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from authentication.views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('authentication.urls')),
    path('author/', include('author.urls')),
    path('book/', include('book.urls')),
    path('order/', include('order.urls')),
    path('librarian/', include('authentication.urls')),

    #path('api-auth', include('rest_framework.urls')),
    path('api-auth/', AuthenticatedView.as_view()),
    path('api/v1/author/', include('author.rest_urls')),
    path('api/v1/user/', include('authentication.rest_urls')),
    path('api/v1/book/', include('book.rest_urls')),
    path('api/v1/order/', include('order.rest_urls')),
]
