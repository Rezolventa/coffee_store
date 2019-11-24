from django.shortcuts import render, redirect, reverse
from django.views.generic import View

from .models import Item, Order, OrderRow
from .forms import ItemForm, OrderForm
from . import utils

from django.http import HttpResponse
import json


def items_list(request):
    items = Item.objects.all()
    return render(request, 'retail/index.html',  context={'items': items})


def get_current_order():
    return Order.objects.filter(client_id=client_id, status=0).last()


def add_to_cart(request):
    # ищем последний заказ в драфте по данному клиенту
    order = Order.objects.filter(client_id=client_id, status=0).last()

    # если его нет, создаем
    if not order:
        order = Order(client_id=client_id, status=0)
        order.save()

    data = json.loads(request.body)
    item = Item.objects.get(id__iexact=str(data.get('item_id')))
    count = data.get('weight')

    order.add_row(item, count)
    return HttpResponse(status=204)


class ItemCreate(View):
    def get(self, request):
        form = ItemForm()
        return render(request, 'retail/item_create.html', context={'form': form})


    def post(self, request):
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save()
            return redirect('items_list_url')
        return render(request, 'retail/item_create.html', context={'form': form})


class ItemEdit(View):
    def get(self, request, id):
        item = Item.objects.get(id__iexact=id)
        form = ItemForm(instance=item)
        return render(request, 'retail/item_edit_form.html', context={'form': form, 'item': item})


    def post(self, request, id):
        item = Item.objects.get(id__iexact=id)
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('items_list_url')
        return render(request, 'retail/item_edit_form.html', context={'form': form, 'item': item})


class ItemDelete(View):
    def get(self, request, id):
        item = Item.objects.get(id__iexact=id)
        form = ItemForm(instance=item)
        return render(request, 'retail/item_delete_form.html', context={'form': form, 'item': item})


    def post(self, request, id):
        item = Item.objects.get(id__iexact=id)
        item.delete()
        return redirect('items_list_url')


class OrderEdit(View):
    def get(self, request):
        order = get_current_order()
        if not order:
            form = OrderForm()
        else:
            form = OrderForm(instance=order)
        order_table = OrderRow.objects.filter(order=order)

        if order_table.count() == 0:
            return redirect('items_list_url') # TODO: проинформировать пользователя о том, что корзина пуста
                                              #       на клиенте без обновления страницы
        data = order.get_full_amount()
        return render(request, 'retail/cart.html', context={'form': form, 'order_table': order_table, 'data': data})

    def post(self, request):
        order = get_current_order()
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save() # сохранение order
            order.close()
            return render(request, 'retail/order_closing_form.html')
        return redirect('order_edit_url')


# константа, заменяющие id клиента и текущий заказ
client_id = '1'

# очистка заказов
utils.clear_obj(Order)
utils.clear_obj(OrderRow)