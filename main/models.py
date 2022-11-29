from django.db import models
from django.contrib.postgres.fields import ArrayField

class Category(models.Model):
    slug = models.SlugField()
    public_name = models.CharField(max_length=50)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None) #cначала одна запись, потом доб. эту колонку
    image = models.ImageField(upload_to='images')
    show = models.BooleanField(default=True)

class Product(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    images = ArrayField(models.ImageField(upload_to='images'), size=7)
    code = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True)
    is_new = models.BooleanField(default=True)
    description = models.TextField()
    show = models.BooleanField(default=True)
    # colors = ArrayField(models.CharField(max_length=20), size=20)
    # sizes = ArrayField(models.CharField(max_length=20), size=20)

class Amount(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    amount = models.IntegerField()