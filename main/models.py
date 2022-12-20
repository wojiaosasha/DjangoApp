from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from .utils import slugify, SingletonModel, ContactsChoices, Cart

class Category(models.Model):
    slug = models.SlugField(editable=False, default='slug')
    is_leaf = models.BooleanField(editable=False, default=True)
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, blank=True) #cначала одна запись, потом доб. эту колонку
    image = models.ImageField(upload_to='images/categories') #, default='back.png', blank=True
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.parent:
            self.parent.is_leaf = False
            self.parent.save()
        super().save(*args, **kwargs)

    @property
    def get_path(self):
        path = []
        node = self
        while node:
            path.insert(0, node)
            node = node.parent
        return path

    @property
    def children(self):
        return Category.objects.filter(parent_id=self.pk)

    @property
    def products(self):
        if self.is_leaf:
            return Product.objects.filter(product_info_id__in=ProductInfo.objects.filter(category_id=self.pk).values_list('id',flat=True))
        else: 
            result = Category.objects.none()
            for i in Category.objects.filter(parent_id=self.pk):
                result |= i.products
            return result

    # @property
    # def is_leaf(self):
    #     return not Category.objects.filter(parent_id=self.pk).first()

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/products')

    def __str__(self):
        return self.image.name

class ProductInfo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, limit_choices_to={'is_leaf':True})
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    images = models.ManyToManyField(ProductImage, blank=True) #max 6

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.IntegerField()
    product_info = models.ForeignKey(ProductInfo, on_delete=models.PROTECT) ##
    color = models.CharField(max_length=30) #
    title_image = models.ImageField(upload_to='images/products')#
    sizes = ArrayField(models.CharField(max_length=20), size=10, null=True, blank=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product_info.name}, {self.color}"

    @property
    def category_path(self):
        list = []
        item = Category.objects.filter(pk=self.product_info.category_id).first()
        while item:
            list = [item] + list
            item = Category.objects.filter(pk=item.parent_id).first()
        return list

    @property
    def color_vars(self):
        return Product.objects.filter(product_info_id=self.product_info.pk)

    @property
    def is_new(self):
        new_products = list(Product.objects.order_by('id').reverse().values_list('id', flat=True))[:10]
        return self.pk in new_products
    
    @property
    def name(self):
        return self.product_info.name

    @property
    def description(self):
        return self.product_info.description

    @property
    def price(self):
        return self.product_info.discount_price if self.product_info.discount_price else self.product_info.price

    @property
    def is_discount(self):
        return bool(self.product_info.discount_price)

    @property
    def images(self):
        return self.product_info.images.all

class Amount(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    size = models.CharField(max_length=20, null=True, blank=True)
    amount = models.IntegerField(default=0)
    ordered = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}, {self.product.color}, {self.size}"

# class AdminUser(User):
#     groups = None
#     user_permissions = None
#     is_staff = None

class CustomUser(models.Model):
    phone = models.BigIntegerField(unique=True)
    code = models.CharField(max_length=4, null=True, default=None, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, default=None)

    name = models.CharField(max_length=50, default='', blank=True)
    email = models.EmailField(default='', blank=True)

    favorite = models.ManyToManyField(Product, blank=True)
    # old_cart =  models.ManyToManyField(Amount, blank=True)
    # cart_amounts = ArrayField(models.IntegerField(default=1), default=list, blank=True) #определить он делит

    def __str__(self):
        return str(self.phone)

    def check_code(self, code=None):
        if self.code == code:
            return True
        else:
            return False

    def change_cart(self, variation: Amount, amount=1):
        
        if variation:
            if amount > 0:
                # cart_item, _ = Cart.objects.get_or_create(user_id=self.pk, product_id=variation.pk)
                cart_item, _ = self.cart.get_or_create(user_id=self.pk, product_id=variation.pk)
                cart_item.amount = amount
                cart_item.save()
            else:
                self.cart.filter(product_id=variation.pk).delete()
                # Cart.objects.delete(user_id=self.pk, product_id=variation.pk)
                
    def change_favorite(self, product: Product = None, delete=False):
        if product:
            if delete:
                self.favorite.remove(product)
            else:
                self.favorite.add(product)
            product.save()
                
    @property
    def is_authenticated(self):
        return True

    @property
    def cart_amount(self):
        return sum([i.amount for i in self.cart.all()])
    
    @property
    def cart_full_price(self):
        full_price = 0
        for i in self.cart.all():
            full_price += i.product.product.price * i.amount
        return full_price

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Amount, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user}: {self.product}, {self.amount}"

class InfoPageImage(models.Model):
    image = models.ImageField(upload_to='images/infopages')

    def __str__(self):
        return self.image.name

class InfoPage(models.Model):
    slug = models.SlugField(editable=False, default='slug')
    title = models.CharField(max_length=20)
    title_image = models.ImageField(upload_to='images/infopages', null=True, blank=True)
    text_area_1 = models.TextField()
    images = models.ManyToManyField(InfoPageImage, blank=True)
    text_area_2 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

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

    def __str__(self):
        return "Settings"

class Contact(models.Model):
    name = models.CharField(max_length=20, choices=ContactsChoices.choices)
    link = models.URLField()

    def __str__(self):
        return self.name

    @property
    def icon(self):
        return 'img/contact_icons/' + self.name + '.svg'

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    phone = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.EmailField()
    products = models.ManyToManyField(Amount) #строка/массив строк?
    amounts = ArrayField(models.IntegerField())
    date = models.DateTimeField()
    delivery = models.TextField(null=True)
    #date
    #способ доставки
