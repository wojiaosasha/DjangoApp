from django.shortcuts import render as django_render, redirect
from django.http import HttpResponse
from .models import Category, Product, CustomUser, Amount, InfoPage, Contact, SiteSettings, ProductInfo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login as login_user, logout as logout_user

from .utils import slugify, create_code, ContactsChoices
from .backends import AuthBackend

#везде добавить show true

def base_info(request):
    categories = Category.objects.filter(parent_id=None)
    infopages = InfoPage.objects.all()
    user = request.user
    settings = SiteSettings.load()
    whatsapp = Contact.objects.filter(name=ContactsChoices.WHATSAPP).first()
    instagram = Contact.objects.filter(name=ContactsChoices.INSTAGRAM).first()
    contacts = Contact.objects.exclude(name=ContactsChoices.WHATSAPP)
    return {
        'infopages' : infopages, 
        'user' : user, 
        'settings' : settings, 
        'whatsapp' : whatsapp, 
        'contacts' : contacts, 
        'instagram' : instagram,
        'categories' : categories,
        }

def page_404(request):
    return render(request, 'main/404.html')

def render(request, str, arr={}):
    return django_render(request, str, arr | base_info(request))

def index(request): #add random

    # print(request.user.cart)

    title_categories = Category.objects.all()[:5]

    new_products = Product.objects.all()[:10]

    info = {'title_categories' : title_categories, 'new_products' : new_products}

    # for i in title_categories:
    #     print(i.name)

    return render(request, 'main/index.html', info)

def infopage(request, slug = ''):
    infopage = InfoPage.objects.filter(slug=slug).first()
    if infopage:
        return render(request, 'main/infopage.html', {'page' : infopage})
    else:
        return HttpResponse("<h1>Страницы не существует</h1>")

def catalog(request):
    products = Product.objects.filter(show = True)

    info = {'products' : products}
    return render(request, 'main/catalog.html', info)

def category(request, slug = ''): #чота висит

    category = Category.objects.filter(slug = slug).first()
    if category:
        products = category.products
        info = {'products': products, 'category' : category}
        return render(request, 'main/category.html', info)
    else: 
        return page_404(request)

def search(request):
    q = request.GET.get('q', None)

    if q:
        by_description = Product.objects.filter(product_info_id__in=ProductInfo.objects.filter(description__icontains = q))
        by_name = Product.objects.filter(product_info_id__in=ProductInfo.objects.filter(name__icontains = q))
        by_code = Product.objects.filter(code__icontains = q)
        by_color = Product.objects.filter(color__icontains = q)

        products = by_description | by_name | by_code | by_color
    
    # in_name = Product.objects.filter(name__icontains = q)
    # in_description = Product.objects.filter(description__icontains = q)
    # in_code = Product.objects.filter(code__icontains = q)

    # products = in_name | in_description | in_code

        if products:
            info = {'products' : products, 'q': q}

            return render(request, 'main/search.html', info)
    # else:
    return render(request, 'main/badsearch.html', {'q': q})

def product(request, number = 0):
    product = Product.objects.filter(code = number).first()

    if product:
        info = {'product': product}

        #user_count

        return render(request, 'main/product.html', info)

    else:
        return page_404(request)

def getcode(request):
    if request.method == 'POST':
        phone = int(request.POST.get('phone', 0))
        user, _ = CustomUser.objects.get_or_create(phone=phone)

        generated_code = create_code()

        #отправляем куда-то
        print(f'code: {generated_code}')

        user.code = generated_code
        user.save()

        # # print(redirect(request.META.get('HTTP_REFERER', reverse('main'))+'#openModal5', phone=user.phone).__dict__)
        # response = redirect(request.META.get('HTTP_REFERER', reverse('main'))+'#openModal5', phone=user.phone)
        # response.headers['phone'] = user.phone

        # print(response.__dict__)

        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main'))+'#openModal5')
        response.headers['phone'] = user.phone
        # response.META['phone'] = user.phone

        # print(response.__dict__)

        return response
    # return HttpResponseRedirect(reverse('main')+'#openModal5')

def login(request):
    if request.method == 'POST':
        phone = int(request.POST['phone'])
        code = request.POST['code']
        # return HttpResponse(f'<h1>{phone}</h1>')
        if True: #валидация данных
            user = AuthBackend.authenticate(None, phone=phone, code=code)
            # return HttpResponse(f'<h1>{user}</h1>')
            if user is not None:
                if user.is_active:
                    login_user(request, user, 'main.backends.AuthBackend')
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    # else:
    #     form = LoginForm()
    # return render(request, 'account/login.html', {'form': form})

def logout(request):
    logout_user(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main')))

def cart(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'cart'):
            if request.method == 'GET':
                # cart = request.user.get_cart
                return render(request, 'main/cart.html')#, {'cart' : cart})
            elif request.method == 'POST':
                variation = None
                id = request.POST.get('id', False)
                amount = int(request.POST.get('amount', 0))
                if id:
                    variation = Amount.objects.filter(pk=id).first()
                else:
                    code = int(request.POST.get('code', False))
                    size = request.POST.get('size', None)
                    product = Product.objects.filter(code=code).first()
                    if product:
                        variation = Amount.objects.filter(product_id=product.pk, size=size).first()
                if variation:
                    request.user.change_cart(variation, amount)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main')))

def favorite(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'cart'):
            if request.method == 'GET':
                favorite = request.user.favorite.all()
                return render(request, 'main/favorite.html', {'favorite' : favorite})
            elif request.method == 'POST':
                code = int(request.POST.get('code', None))
                delete = bool(request.POST.get('delete', None))
                product = Product.objects.filter(code=code).first()
                if product:
                    if delete:
                        request.user.change_favorite(product, delete=True)
                    else:
                        request.user.change_favorite(product) #дописать гет атрибутов и параметры
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main')))

def order(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'cart'):
            if request.method == 'GET':
                if request.user.cart.all():
                    return render(request, 'main/order.html')
            elif request.method == 'POST':
                name = request.POST.get('name', None)
                email = request.POST.get('email', None)
                phone = request.POST.get('phone', None)
                delivery = request.POST.get('delivery', None)
                adress = ''
                if delivery:
                    data_fields = ['index', 'town', 'street', 'house', 'apart', 'comment']
                    for i in data_fields:
                        field = request.POST.get(i, None)
                        if field != data_fields[-1]:
                            adress += f'{field}, '
                        else:
                            adress += field
                else:
                    adress = None
                #проверить наличие товаров и создать заказ

                for i in request.user.cart.all():
                    # print(i)
                    if i.amount > Amount.objects.filter(pk=i.product_id).first().amount:
                        return HttpResponse('мало товаров')

                
                return render(request, 'main/success.html')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main')))