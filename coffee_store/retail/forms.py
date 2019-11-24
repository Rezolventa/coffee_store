from django import forms
from .models import Item, Order

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'})
        }

# в ордере пользователь ничего особо вводить не будет - кроме своего номера телефона
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'})
        }