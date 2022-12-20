from django.contrib import admin
from .models import Category, Product, Amount, CustomUser, InfoPage, ProductImage, InfoPageImage, Contact, SiteSettings, ProductInfo, Order
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
admin.site.register(Category)
admin.site.register(Amount)
admin.site.register(CustomUser)
admin.site.register(InfoPage)
admin.site.register(ProductImage)
admin.site.register(InfoPageImage)
admin.site.register(ProductInfo)
admin.site.register(Order)

class YourModelForm(forms.ModelForm):

    # extra_field = forms.ImageField(required=False)
    # ex = forms.ImageField(required=False)
    # sizes = SimpleArrayField(forms.CharField(max_length=20, required=False), delimiter=',')
    # colors = SimpleArrayField(forms.CharField(max_length=20, required=False), delimiter=',')

    def save(self, commit=True):
        #print(commit)
        product = super().save(commit=False)

        sizes = product.sizes
        # sizes = self.cleaned_data.get('sizes', None)
    
        # path = default_storage.save('images/' + filename, ContentFile(f1.read()))
        # newpath = settings.MEDIA_ROOT + '/' + path
        # imf = ImageFieldFile(instance=Product, field=models.ImageField(), name='images/'+filename)

        #if commit: #?? при создании commit+True, редактирование commit=False или наоборот
        
        product.save()

        # проверка на уменьшение количества атрибутов
        if sizes:
            for size in sizes:
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
    list_display = ['code', 'color']

    form = YourModelForm