from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from .utils import slugify, SingletonModel, ContactsChoices

class Category(models.Model):
    slug = models.SlugField(editable=False, default='slug')
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, blank=True) #cначала одна запись, потом доб. эту колонку
    image = models.ImageField(upload_to='images/categories', null=True)
    show = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/products')

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    #is_new = models.BooleanField(default=True)
    description = models.TextField()
    show = models.BooleanField(default=True)
    images = models.ManyToManyField(ProductImage, blank=True)
    colors = ArrayField(models.CharField(max_length=20), size=20, null=True, default=None, blank=True)
    sizes = ArrayField(models.CharField(max_length=20), size=20, null=True, default=None, blank=True)

    def get_color_index(self, color):
        return self.colors.index(color)#??????

    @property
    def category_path(self):
        list = []
        item = Category.objects.filter(pk=self.category_id).first()
        while item:
            list = [item] + list
            item = Category.objects.filter(pk=item.parent_id).first()
        return list

    @property
    def is_new(self):
        new_products = list(Product.objects.order_by('id').reverse().values_list('id', flat=True))[:10]
        return self.pk in new_products

class Amount(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    ordered = models.IntegerField(default=0)

# class AdminUser(User):
#     groups = None
#     user_permissions = None
#     is_staff = None

class CustomUser(models.Model):
    phone = models.BigIntegerField(unique=True)
    code = models.CharField(max_length=4, null=True, default=None, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, default=None)

    favorite = models.ManyToManyField(Product, blank=True)
    cart =  models.ManyToManyField(Amount, blank=True)
    cart_amounts = ArrayField(ArrayField(models.IntegerField(default=0), default=list), default=list, size=2, blank=True) #определить он делит

    def check_code(self, code=None):
        if self.code == code:
            return True
        else:
            return False

    def add_to_cart(self, variation: Amount, amount=1):
        if variation:
            self.cart.add(variation)
            if not self.cart_amounts:
                self.cart_amounts = [[variation.pk], [amount]]
            else:
                if self.cart_amounts[0].__contains__(variation.pk):
                    self.cart_amounts[1][self.cart_amounts[0].index(variation.pk)] += amount
                else:
                    self.cart_amounts[0].append(variation.pk)
                    self.cart_amounts[1].append(amount)
            self.save()
                
    @property
    def is_authenticated(self):
        return True

    @property
    def cart_amount(self):
        return self.cart.all().count()
    
    @property
    def cart_full_price(self):
        return sum([i.product.price for i in self.cart.all()])

class InfoPageImage(models.Model):
    image = models.ImageField(upload_to='images/infopages')

class InfoPage(models.Model):
    slug = models.SlugField(editable=False, default='slug')
    title = models.CharField(max_length=20)
    title_image = models.ImageField(upload_to='images/infopages', null=True, blank=True)
    text_area_1 = models.TextField()
    images = models.ManyToManyField(InfoPageImage, blank=True)
    text_area_2 = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class SiteSettings(SingletonModel):
    phone = models.CharField(max_length=12, null=True)
    email = models.EmailField(null=True)
    privacy_policy = models.FileField(upload_to='documents', null=True) #add validators??
    terms_of_use = models.FileField(upload_to='documents', null=True) #add validators??
    main_caterories = models.ManyToManyField(Category)
    title_image = models.ImageField(upload_to='images/title', null=True, blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=20, choices=ContactsChoices.choices)
    link = models.URLField()

    @property
    def icon(self):
        return 'img/contact_icons/' + self.name + '.svg'