# project/forms.py
# Amy Ho, aho@bu.edu

from django import forms
from .models import Category, Item, PurchaseRecord, UsageRecord
from django.utils import timezone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'current_quantity', 'minimum_quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PurchaseRecordForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecord
        fields = ['item', 'purchase_date', 'quantity', 'unit_cost']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase_date'].initial = timezone.now().date()

class UsageRecordForm(forms.ModelForm):
    class Meta:
        model = UsageRecord
        fields = ['item', 'usage_date', 'quantity_used']
        widgets = {
            'usage_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usage_date'].initial = timezone.now().date()