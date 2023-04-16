from django.contrib import admin 
from django.urls import path 
from . import views

app_name = 'grocery_list'

urlpatterns = [
    path('', views.home, name='home'),
    path('new_list', views.create_list, name="create_list"),
]