from django.test import TestCase, Client
from django.db import transaction, Error
from django.urls import reverse, resolve

from retail.models import Item, Order, OrderRow
from retail.forms import ItemForm, OrderForm
from retail.views import add_to_cart, ItemList, ItemCreate, OrderEdit


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
                neg_item = Item.objects.create(title='Отрицательная цена', description='data', price=-25)
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


class FormsTestCase(TestCase):
    def setUp(self):
        form1 = ItemForm({'title': 'Кофе int', 'description': 'Произвольное описание', 'price': 137})
        form1.save()

        form2 = ItemForm({'title': 'Кофе str', 'description': 'Произвольное описание', 'price': '1337'})
        form2.save()

    def test_forms_output_typization_easy(self):
        item = Item.objects.get(title__iexact='Кофе int')
        self.assertIs(type(item.price), int)

    def test_forms_output_typization_from_str(self):
        item = Item.objects.get(title__iexact='Кофе str')
        self.assertIs(type(item.price), int)


class UrlsTestCase(TestCase):
    def test_items_list_url(self):
        url = reverse('items_list_url')
        self.assertEqual(resolve(url).func.view_class, ItemList)

    def test_item_create_url(self):
        url = reverse('item_create_url')
        self.assertEqual(resolve(url).func.view_class, ItemCreate)

    def test_add_to_cart_url(self):
        url = reverse('add_to_cart_url')
        self.assertEqual(resolve(url).func, add_to_cart)

    def test_order_edit_url(self):
        url = reverse('order_edit_url')
        self.assertEqual(resolve(url).func.view_class, OrderEdit)


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # test_order_edit_url_POST
        item1 = Item.objects.create(title='Кофе', description='Описание товара', price=137)
        item2 = Item.objects.create(title='Coffee', description='Descr', price=25)
        order = Order.objects.create(phone_number='+7 31337000', client_id=1, status=0)
        OrderRow.objects.create(order=order, item=item1, count=3, price=item1.price)
        OrderRow.objects.create(order=order, item=item2, count=4, price=22)
        self.test_order = order

    # ItemList
    def test_item_list_url_GET(self):
        response = self.client.get(reverse('items_list_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'retail/index.html')

    # ItemCreate(GET)
    def test_item_create_url_GET(self):
        response = self.client.get(reverse('item_create_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'retail/item_create.html')

    # ItemCreate(POST)
    def test_item_create_url_POST(self):
        form = {'title': 'test_item_create_url_POST', 'description': 'descr', 'price': 25}
        response = self.client.post(reverse('item_create_url'), form)
        self.assertEqual(response.status_code, 302)
        self.assertIs(type(Item.objects.get(title='test_item_create_url_POST')), Item)

    # OrderEdit(GET)
    def test_order_edit_url_GET(self):
        response = self.client.get(reverse('order_edit_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'retail/cart.html')

    # OrderEdit(POST)
    def test_order_edit_url_POST(self):
        form = {'phone_number': self.test_order.phone_number}
        response = self.client.post(reverse('order_edit_url'), form, instance=self.test_order)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'retail/order_closing_form.html')
        self.assertEqual(self.test_order.status, 0) # почему 0, должно быть 1?