from django.test import TestCase
from django.db import transaction, Error
from django.urls import reverse, resolve

from .models import Item, Order, OrderRow
from .forms import ItemForm, OrderForm
from .views import items_list


class ModelsTestCase(TestCase):
    test_flag = False

    def setUp(self):
        # test_item_create_easy
        item1 = Item.objects.create(title='Кофе', description='Описание товара', price=137)
        item2 = Item.objects.create(title='%f_123  # !qwertysdфывауце !"№;%:?*()_-=+_ ',
             description='фывауце !"№;%:?*()_-=+_ %f_123  # !qwerty', price=25)

        # test_item_neg_price
        try:
            with transaction.atomic():
                Item.objects.create(title='Отрицательная цена', description='data', price=-25)
        except Error:
            self.test_flag = True

        # test_order_create_easy
        order = Order.objects.create(phone_number='+7 31337', client_id=1, status=0)
        OrderRow.objects.create(order=order, item=item1, count=3, price=item1.price)
        OrderRow.objects.create(order=order, item=item2, count=4, price=22)

    def test_item_create_easy(self):
        test_obj_easy = Item.objects.get(title__iexact='Кофе')
        self.assertIs(type(test_obj_easy), Item)
        self.assertEqual(test_obj_easy.title, 'Кофе')
        self.assertEqual(test_obj_easy.description, 'Описание товара')

        test_obj_symbols = Item.objects.get(price=25)
        self.assertIs(type(test_obj_symbols), Item)

    def test_item_neg_price(self):
        self.assertEqual(self.test_flag, True)

    def test_order_create_easy(self):
        test_obj = Order.objects.get(phone_number='+7 31337')
        self.assertIs(type(test_obj), Order)
        self.assertEqual(test_obj.status, 0)

        row_list = OrderRow.objects.filter(order=test_obj)
        self.assertEqual(row_list.count(), 2)

# need to be edited
class FormsOutputTypizationTestCase(TestCase):
    def setUp(self):
        form = ItemForm({'title': 'Кофе', 'description': 'Произвольное описание', 'price': '1337'})
        form.save()

    def test_something(self):
        item = Item.objects.get(title__iexact='Кофе')
        self.assertIs(type(item.price), int)


class TestUrls(TestCase):
    def test_items_list_url(self):
        url = reverse('items_list_url')
        self.assertEqual(resolve(url).func, items_list)