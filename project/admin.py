# project/admin.py
# Amy Ho, aho@bu.edu

from django.contrib import admin

# Register your models here.
from .models import Category, Item, PurchaseRecord, UsageRecord

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(PurchaseRecord)
admin.site.register(UsageRecord)