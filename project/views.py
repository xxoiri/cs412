# project/views.py
# Amy Ho, aho@bu.edu

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q, Sum, F
from .models import Category, Item, PurchaseRecord, UsageRecord
from .forms import CategoryForm, ItemForm, PurchaseRecordForm, UsageRecordForm
from django.shortcuts import redirect
from django.contrib import messages
import plotly.graph_objs as go
from plotly.offline import plot
from django.db.models.functions import TruncMonth


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

# Item Views
class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'project/item_list.html'
    
    def get_queryset(self):
        queryset = Item.objects.select_related('category').all()
        
        # Get search parameter from GET request
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        # Get category filter from GET request
        category_filter = self.request.GET.get('category')
        if category_filter and category_filter != 'all':
            queryset = queryset.filter(category_id=category_filter)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        
        # Add category filter to context
        context['selected_category'] = self.request.GET.get('category', 'all')
        
        # Add all categories for filter dropdown
        context['all_categories'] = Category.objects.all()
        
        return context

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
    '''View to display purchase records with analytics.'''
    
    model = PurchaseRecord
    context_object_name = 'purchases'
    template_name = 'project/purchaserecord_list.html'

    def get_queryset(self):
        qs = PurchaseRecord.objects.select_related('item', 'item__category')
        
        # Apply search filter
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(item__name__icontains=search) | 
                Q(item__category__name__icontains=search)
            )
        
        # Apply category filter
        category = self.request.GET.get('category')
        if category and category != 'all':
            qs = qs.filter(item__category_id=category)
        
        return qs.order_by('-purchase_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filtered purchases
        purchases = context['purchases']
        
        # Calculate simple totals
        total_spent = sum(p.quantity * p.unit_cost for p in purchases)
        
        # Create ONE simple chart
        context['monthly_chart'] = self.create_monthly_chart(purchases)
        
        # Add filter options
        context['all_categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', 'all')
        context['search_query'] = self.request.GET.get('search', '')
        context['total_spent'] = total_spent
        
        # Add total_cost for each purchase
        for purchase in purchases:
            purchase.total_cost = purchase.quantity * purchase.unit_cost
        
        return context

    def create_monthly_chart(self, purchases):
        '''Create a simple monthly spending chart'''
        # Group by month
        monthly_data = purchases.annotate(
            month=TruncMonth('purchase_date')
        ).values('month').annotate(
            total=Sum(F('quantity') * F('unit_cost'))
        ).order_by('month')
        
        # Extract data
        months = []
        totals = []
        
        for entry in monthly_data:
            months.append(entry['month'].strftime('%b %Y'))
            totals.append(float(entry['total'] or 0))
        
        # Create chart if we have data
        if totals:
            fig = go.Bar(
                x=months, 
                y=totals,
                marker_color='#667eea'
            )
            
            layout = go.Layout(
                title="Monthly Spending",
                xaxis_title="Month",
                yaxis_title="Amount ($)",
                showlegend=False
            )
            
            graph_div = plot(
                {"data": [fig], "layout": layout},
                auto_open=False,
                output_type="div"
            )
            return graph_div
        
        return None

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
    
    def get_queryset(self):
        return UsageRecord.objects.select_related('item', 'item__category').order_by('-usage_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Simple calculations
        usage_records = context['usage_records']
        total_used = usage_records.aggregate(total=Sum('quantity_used'))['total'] or 0
        
        context['total_used'] = total_used
        context['unique_items'] = usage_records.values('item').distinct().count()
        
        return context


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