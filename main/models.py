from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

