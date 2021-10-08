from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'number_of_people', 'start_date', 'end_date', 'room', 'user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'room': forms.HiddenInput(attrs={'readonly': True}),
            'user': forms.HiddenInput(attrs={'readonly': True}),
        }
