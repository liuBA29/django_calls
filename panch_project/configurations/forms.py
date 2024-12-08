from django import forms
from .models import *


from django import forms
from .models import Client, ContactInfo

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['phone', 'email', 'address']

class ClientForm(forms.ModelForm):
    contact_info_phone = forms.CharField(max_length=20, required=False)
    contact_info_email = forms.EmailField(required=False)
    contact_info_address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Client
        fields = ['name', 'image', 'is_active']

    def save(self, commit=True):
        instance = super().save(commit=False)

        contact_info_data = {
            'phone': self.cleaned_data['contact_info_phone'],
            'email': self.cleaned_data['contact_info_email'],
            'address': self.cleaned_data['contact_info_address']
        }

        # Create or update the ContactInfo instance
        contact_info, created = ContactInfo.objects.get_or_create(
            phone=contact_info_data['phone'],
            email=contact_info_data['email'],
            address=contact_info_data['address']
        )
        instance.contact_info = contact_info

        if commit:
            instance.save()

        return instance
