"""blv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from pyq import views

urlpatterns = [
    path('', views.pyqs_init, name='pyqs'),
    path('get_result_all/', views.get_result_all),
    path('get_result_img/', views.get_result_img),
    path('get_free_chat/', views.get_free_chat),
    path('pyqs/<int:pyq_id>/', views.pyq_detail, name='pyq_index'),
]
