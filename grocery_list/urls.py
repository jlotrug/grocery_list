from django.contrib import admin 
from django.urls import path 
from . import views

app_name = 'grocery_list'

urlpatterns = [
    path('', views.home, name='home'),
    path('new_list', views.create_list, name="create_list"),
    path('<int:id>', views.grocery_list, name='g_list'),
    path('item/<int:id>', views.item_details, name='item'),
    path('create_item', views.create_item, name='create_item'),
    path('all_items', views.all_items, name='all_items'),
    path('edit/<int:id>', views.edit_item, name='edit'),
]