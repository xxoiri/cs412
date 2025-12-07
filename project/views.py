# project/views.py
# Amy Ho, aho@bu.edu

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Category, Item, PurchaseRecord, UsageRecord
from .forms import CategoryForm, ItemForm, PurchaseRecordForm, UsageRecordForm

# Category Views
class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('project:category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('project:category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('project:category-list')
    template_name_suffix = '_confirm_delete'

# Item Views
class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    
    def get_queryset(self):
        return Item.objects.select_related('category').all()

class ItemDetailView(DetailView):
    model = Item

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('project:item-list')

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('project:item-list')

class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('project:item-list')
    template_name_suffix = '_confirm_delete'

# PurchaseRecord Views
class PurchaseRecordListView(ListView):
    model = PurchaseRecord
    context_object_name = 'purchases'

class PurchaseRecordCreateView(CreateView):
    model = PurchaseRecord
    form_class = PurchaseRecordForm
    success_url = reverse_lazy('project:purchase-list')

class PurchaseRecordUpdateView(UpdateView):
    model = PurchaseRecord
    form_class = PurchaseRecordForm
    success_url = reverse_lazy('project:purchase-list')

class PurchaseRecordDeleteView(DeleteView):
    model = PurchaseRecord
    success_url = reverse_lazy('project:purchase-list')
    template_name_suffix = '_confirm_delete'

# UsageRecord Views
class UsageRecordListView(ListView):
    model = UsageRecord
    context_object_name = 'usage_records'

class UsageRecordCreateView(CreateView):
    model = UsageRecord
    form_class = UsageRecordForm
    success_url = reverse_lazy('project:usage-list')

class UsageRecordUpdateView(UpdateView):
    model = UsageRecord
    form_class = UsageRecordForm
    success_url = reverse_lazy('project:usage-list')

class UsageRecordDeleteView(DeleteView):
    model = UsageRecord
    success_url = reverse_lazy('project:usage-list')
    template_name_suffix = '_confirm_delete'