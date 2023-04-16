from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_carbs = models.CharField(max_length=200)
    item_fat = models.CharField(max_length=200)
    item_protein = models.CharField(max_length=200)
    item_calories = models.CharField(max_length=200)
    item_notes = models.CharField(max_length=800)
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=500, default="https://liftlearning.com/wp-content/uploads/2020/09/default-image.png")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class List(models.Model):
    list_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ListItem(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    list_id = models.ForeignKey(List, on_delete=models.CASCADE)
