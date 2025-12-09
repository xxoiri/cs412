# project/models.py
# Amy Ho, aho@bu.edu

from django.db import models
# Create your models here.

class Category(models.Model):
    '''Categories for the types of items. '''
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def get_all_items(self):
        '''returns items within a category'''
        return self.item_set.all()
    
    def item_count(self):
        '''returns count of items in this category'''
        return self.item_set.count()
    
    def low_stock_count(self):
        '''returns count of low stock items in category'''
        count = 0
        for item in self.item_set.all():
            if item.current_quantity <= item.minimum_quantity:
                count += 1
        return count


class Item(models.Model):
    '''Represents the items that we want to purchase/already have.'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    current_quantity = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class PurchaseRecord(models.Model):
    '''See which items we have purchased already.'''
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateField()
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.item.name} - {self.quantity} on {self.purchase_date}"
    
    def get_all_history(self):
        '''returns all purchase records for this item'''
        return self.item.purchases.all().order_by('-purchase_date')


class UsageRecord(models.Model):
    '''Items that we are using/have used.'''
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="usage_records")
    usage_date = models.DateField()
    quantity_used = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.item.name} - used {self.quantity_used} on {self.usage_date}"
    
    def get_all_usage(self):
        '''returns all usage records for this item'''
        return self.item.usage_records.all().order_by('-usage_date')
