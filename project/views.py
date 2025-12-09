# project/views.py
# Amy Ho, aho@bu.edu

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Category, Item, PurchaseRecord, UsageRecord
from .forms import CategoryForm, ItemForm, PurchaseRecordForm, UsageRecordForm
from django.shortcuts import redirect
from django.contrib import messages

# Home Page
class HomeView(TemplateView):
    '''Main dashboard view showing inventory overview.'''
    template_name = 'project/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all items with their categories
        items = Item.objects.select_related('category').all()
        context['total_items'] = items.count()
        context['total_categories'] = Category.objects.count()
        
        # Calculate low stock items
        low_stock_items = []
        for item in items:
            if item.current_quantity <= item.minimum_quantity:
                low_stock_items.append(item)
        context['low_stock_items'] = low_stock_items
        context['low_stock_count'] = len(low_stock_items)
        
        # Recent activity
        context['recent_purchases'] = PurchaseRecord.objects.select_related('item').order_by('-purchase_date')[:5]
        context['recent_usage'] = UsageRecord.objects.select_related('item').order_by('-usage_date')[:5]
        
        # All categories
        context['categories'] = Category.objects.all()
        
        return context

# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'project/show_all_categories.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'project/show_category.html'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'project/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'project/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    template_name = 'project/category_confirm_delete.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Check if category has items
        if self.object.item_set.count() > 0:
            # Reassign to another category
            new_category_id = request.POST.get('new_category')
            if new_category_id:
                new_category = Category.objects.get(id=new_category_id)
                self.object.item_set.update(category=new_category)
                messages.success(request, f'Items moved to {new_category.name}')
            
            # Delete all items
            elif request.POST.get('delete_items') == 'true':
                self.object.item_set.all().delete()
                messages.warning(request, 'All items in category deleted')
            
            else:
                # Show error if no action chosen
                messages.error(request, 'Category has items. Choose an action.')
                return redirect('category-delete', pk=self.object.pk)
        
        # Delete
        self.object.delete()
        messages.success(request, 'Category deleted successfully')
        return redirect(self.success_url)

# Item Views
class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'project/item_list.html'
    
    def get_queryset(self):
        return Item.objects.select_related('category').all()

class ItemDetailView(DetailView):
    model = Item
    template_name = 'project/item_detail.html'

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'project/item_form.html'
    success_url = reverse_lazy('item-list')

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'project/item_form.html'
    success_url = reverse_lazy('item-list')

class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('item-list')
    template_name = 'project/item_confirm_delete.html'

# PurchaseRecord Views
class PurchaseRecordListView(ListView):
    model = PurchaseRecord
    context_object_name = 'purchases'
    template_name = 'project/purchaserecord_list.html'
    
    def get_queryset(self):
        return PurchaseRecord.objects.select_related('item', 'item__category').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = context['purchases']
        
        # Calculate totals
        total_quantity = sum(purchase.quantity for purchase in purchases)
        total_spent = sum(purchase.quantity * purchase.unit_cost for purchase in purchases)
        
        context['total_quantity'] = total_quantity
        context['total_spent'] = total_spent
        
        # Also add total_cost for each purchase
        for purchase in purchases:
            purchase.total_cost = purchase.quantity * purchase.unit_cost
        
        return context

class PurchaseRecordCreateView(CreateView):
    model = PurchaseRecord
    form_class = PurchaseRecordForm
    template_name = 'project/purchaserecord_form.html'
    success_url = reverse_lazy('purchase-list')

class PurchaseRecordUpdateView(UpdateView):
    model = PurchaseRecord
    form_class = PurchaseRecordForm
    template_name = 'project/purchaserecord_form.html'
    success_url = reverse_lazy('purchase-list')

class PurchaseRecordDeleteView(DeleteView):
    model = PurchaseRecord
    success_url = reverse_lazy('purchase-list')
    template_name = 'project/purchaserecord_confirm_delete.html'

# UsageRecord Views
class UsageRecordListView(ListView):
    model = UsageRecord
    context_object_name = 'usage_records'
    template_name = 'project/usagerecord_list.html'

class UsageRecordCreateView(CreateView):
    model = UsageRecord
    form_class = UsageRecordForm
    template_name = 'project/usagerecord_form.html'
    success_url = reverse_lazy('usage-list')

class UsageRecordUpdateView(UpdateView):
    model = UsageRecord
    form_class = UsageRecordForm
    template_name = 'project/usagerecord_form.html'
    success_url = reverse_lazy('usage-list')

class UsageRecordDeleteView(DeleteView):
    model = UsageRecord
    success_url = reverse_lazy('usage-list')
    template_name = 'project/usagerecord_confirm_delete.html'