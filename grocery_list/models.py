from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_carbs = models.CharField(max_length=200)
    item_fat = models.CharField(max_length=200)
    item_protein = models.CharField(max_length=200)
    item_calories = models.CharField(max_length=200)
    item_notes = models.CharField(max_length=800, null=True, blank=True)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_image = models.CharField(max_length=500, default="https://liftlearning.com/wp-content/uploads/2020/09/default-image.png")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class List(models.Model):
    list_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='ListItem')

    def __str__(self):
        return self.list_name

class ListItem(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    list_id = models.ForeignKey(List, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_cost(self):
        return self.quantity * self.item_id.item_price
    
    def total_calories(self):
        return self.quantity * int(self.item_id.item_calories)
