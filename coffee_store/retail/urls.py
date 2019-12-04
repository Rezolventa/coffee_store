from django.urls import path

from . import views

from . import utils

urlpatterns = [
    path('', views.ItemList.as_view(), name='items_list_url'),
    path('items/create/', views.ItemCreate.as_view(), name='item_create_url'),
    path('order/', views.OrderEdit.as_view(), name='order_edit_url'),
    path('addtocart/', views.add_to_cart, name='add_to_cart_url'),
    path('items/<str:id>/', views.ItemEdit.as_view(), name='item_edit_url'),
    path('items/<str:id>/delete', views.ItemDelete.as_view(), name='item_delete_url')
]