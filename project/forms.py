# project/forms.py
# Amy Ho, aho@bu.edu

from django import forms
from .models import Category, Item, PurchaseRecord, UsageRecord
from django.utils import timezone

class CategoryForm(forms.ModelForm):
    '''Form to create a new category.'''
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ItemForm(forms.ModelForm):
    '''Form to create new item within a category.'''
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'current_quantity', 'minimum_quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PurchaseRecordForm(forms.ModelForm):
    '''Form to add purchased items into inventory.'''
    class Meta:
        model = PurchaseRecord
        fields = ['item', 'purchase_date', 'quantity', 'unit_cost']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase_date'].initial = timezone.now().date()
    
    def save(self, commit=True):
        '''Override save to update item quantity'''
        purchase = super().save(commit=False)
        
        if commit:
            # Save the purchase first
            purchase.save()
            
            # Update the item's current_quantity
            item = purchase.item
            item.current_quantity += purchase.quantity
            item.save()
        
        return purchase


class UsageRecordForm(forms.ModelForm):
    '''Form to record used items.'''
    class Meta:
        model = UsageRecord
        fields = ['item', 'usage_date', 'quantity_used']
        widgets = {
            'usage_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usage_date'].initial = timezone.now().date()
    
    def clean_quantity_used(self):
        '''Validate that we don't use more than available'''
        quantity_used = self.cleaned_data['quantity_used']
        item = self.cleaned_data.get('item')
        
        if item and quantity_used > item.current_quantity:
            raise forms.ValidationError(
                f"Cannot use {quantity_used} items. Only {item.current_quantity} available."
            )
        
        return quantity_used
    
    def save(self, commit=True):
        '''Override save to update item quantity'''
        usage = super().save(commit=False)
        
        if commit:
            # Save the usage record first
            usage.save()
            
            # Update the item's current_quantity
            item = usage.item
            item.current_quantity -= usage.quantity_used
            item.save()
        
        return usage
