from django.contrib import admin
from .models import Category, Product, Amount, CustomUser, InfoPage, ProductImage, InfoPageImage, Contact, SiteSettings, ProductInfo, Order, Feedback
from django import forms
from django.forms import MultiWidget, TextInput
from django.contrib.postgres.forms import SimpleArrayField
from django.core.files.images import ImageFile

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageFieldFile, FieldFile

admin.site.register(SiteSettings)
admin.site.register(Contact)
admin.site.register(CustomUser)
admin.site.register(InfoPage)
admin.site.register(ProductImage)
admin.site.register(InfoPageImage)
admin.site.register(Order)
admin.site.register(Feedback)

class YourModelForm(forms.ModelForm):

    # extra_field = forms.ImageField(required=False)
    # ex = forms.ImageField(required=False)
    # sizes = SimpleArrayField(forms.CharField(max_length=20, required=False), delimiter=',')
    # colors = SimpleArrayField(forms.CharField(max_length=20, required=False), delimiter=',')

    def save(self, commit=True):
        product = super().save(commit=False)
        
        # sizes = self.cleaned_data.get('sizes', None)
        
        product.save()

        # проверка на уменьшение количества атрибутов
        if product.sizes:
            for size in product.sizes:
                Amount.objects.get_or_create(product_id = product.pk, size=size)
        else:
            Amount.objects.get_or_create(product_id = product.pk, size=None)
        
        return product

    class Meta: #добавляем в форму остальные поля модели
        model = Product
        #exclude = ['images']
        #fields = 'code', 'name'
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'product_info', 'color']

    form = YourModelForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']

@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'amount', 'ordered']

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price']