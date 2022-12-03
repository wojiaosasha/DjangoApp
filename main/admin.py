from django.contrib import admin
from .models import Category, Product, Amount
from django import forms
from django.forms import MultiWidget, TextInput

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Amount)

class YourModelForm(forms.ModelForm):

    #extra_field = forms.CharField(widget=forms.MultiWidget(widgets=[TextInput, TextInput]))
    extra_field = forms.ImageField(required=False)
    ex = forms.ImageField(required=False)

    # widget = MultiWidget(widgets={'': TextInput, 'last': TextInput})
    # widget.render('name', ['john', 'paul'])

    # def save(self, commit=True):
    #     extra_field = self.cleaned_data.get('extra_field', None)
    #     # ...do something with extra_field here...
    #     return super(YourModelForm, self).save(commit=commit)

    def save(self, commit=True):
        instance = super().save(commit=False)

        f1 = self.cleaned_data.get('extra_field', None)
        f2 = self.cleaned_data.get('ex_field', None)

        # [value for value in values if value]

        instance.images = [value for value in [f1, f2] if value]
        if commit:
            instance.save()
            # self.save()
        return instance

    class Meta: #добавляем в форму остальные поля модели
        model = Product
        exclude = ['images']
        #fields = 'code', 'name'
        

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']

    form = YourModelForm

    # fields = ['code', 'name', 'images', 'extra_field'] #отобр. только те поля что будут в форме админки

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'description', 'extra_field',),
    #     }),
    # )
