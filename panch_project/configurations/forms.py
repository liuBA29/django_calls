from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','email','phone', 'image']

    # Вы можете настроить виджет для других полей, например, для телефона или почты
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))