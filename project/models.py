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

class Item(models.Model):
    '''Represents the items that we want to purchase/already have.'''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    current_quantity = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class PurchaseRecord(models.Model):
    '''See which items we have purchased already.'''
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.item.name} - {self.quantity} on {self.purchase_date}"

class UsageRecord(models.Model):
    '''Items that we are using/have used.'''
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    usage_date = models.DateField()
    quantity_used = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.item.name} - used {self.quantity_used} on {self.usage_date}"