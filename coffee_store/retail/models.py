from django.db.models import Sum
from django.shortcuts import reverse
from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True, db_index=True)
    price = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ['title']


    def get_edit_url(self):
        return reverse('item_edit_url', kwargs={'id': self.id})


    def get_delete_url(self):
        return reverse('item_delete_url', kwargs={'id': self.id})


    def __str__(self):
        return str(self.id)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.TimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, db_index=True)
    client_id = models.CharField(max_length=10, db_index=True)
    status = models.IntegerField() # 0 - draft, 1 - negotiating, 2 - closed


    def add_row(self, item, count):
        row = OrderRow.objects.filter(order=self, item=item).first()
        if row:
            row.count = int(row.count) + int(count)
            row.price = round(row.count * item.price / 100)
        else:
            price = round(int(count) * item.price / 100)
            row = OrderRow(order=self, item=item, count=count, price=price)
        row.save()


    def get_view_url(self):
        return reverse('reports_order_url', kwargs={'id': self.id})


    def get_full_amount(self):
        return OrderRow.objects.filter(order=self).aggregate(Sum('price')).get('price__sum')


    def close(self):
        self.status = 1
        self.save()


    def __str__(self):
        return str(self.id)


class OrderRow(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)


    def __str__(self):
        return 'order: {}, item: {}, count: {}, price: {}'.format(self.order, self.item, self.count, self.price)