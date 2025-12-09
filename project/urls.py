# project/views.py
# Amy Ho, aho@bu.edu

from django.urls import path
from .views import *

urlpatterns = [
    # Home
    path('', HomeView.as_view(), name="home-page"),

    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    # Items
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('items/create/', ItemCreateView.as_view(), name='item-create'),
    path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    
    # Purchase Record
    path('purchases/', PurchaseRecordListView.as_view(), name='purchase-list'),
    path('purchases/create/', PurchaseRecordCreateView.as_view(), name='purchase-create'),
    path('purchases/<int:pk>/update/', PurchaseRecordUpdateView.as_view(), name='purchase-update'),
    path('purchases/<int:pk>/delete/', PurchaseRecordDeleteView.as_view(), name='purchase-delete'),
    
    # Usage Record
    path('usage/', UsageRecordListView.as_view(), name='usage-list'),
    path('usage/create/', UsageRecordCreateView.as_view(), name='usage-create'),
    path('usage/<int:pk>/update/', UsageRecordUpdateView.as_view(), name='usage-update'),
    path('usage/<int:pk>/delete/', UsageRecordDeleteView.as_view(), name='usage-delete'),
]