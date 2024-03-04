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
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('setting/', views.setting_view, name='setting'),
    path('', views.pyqs_init, name='pyqs'),

    path('get_result_all/', views.get_result_all),
    path('get_result_img/', views.get_result_img),
    path('get_free_chat/', views.get_free_chat),
    path('get_img_chat/', views.get_img_chat),
    path('pyqs/<int:pyq_id>/', views.pyq_detail, name='pyq_index'),

    path('test/', views.test),
    path('pyqs/<int:pyq_id>/image/<int:img_id>/', views.img_detail, name='img_detail'),

    path('get_img_embedding/', views.img_embedding),
    path('save_image/', views.save_image),
    path('second_layer_explore/', views.second_layer_explore)

    # path('path-to-delete-file/', views.delete_specific_file),
]
