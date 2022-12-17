from django.shortcuts import render as django_render
from django.http import HttpResponse
from .models import Category, Product, CustomUser, Amount, InfoPage, Contact, SiteSettings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login as login_user, logout as logout_user

from .utils import slugify, create_code, ContactsChoices
from .backends import AuthBackend

def base_info(request):
    #корзина инфа
    #инфостраницы, контакты итд

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
        }

def render(request, str, arr={}):
    return django_render(request, str, arr | base_info(request))

def test_url(request):
    if hasattr(request.user, 'phone') and request.user.is_authenticated:
        s = 'Customer'
    else:
        s = 'Хуй в пальто'

    print(slugify('я долбоеб'))

    return render(request, 'main/test.html', {'s' : s, 'pp' : SiteSettings.load().privacy_policy})

def index(request):
    title_categories = Category.objects.all()[:5]

    for i in title_categories:
        print(i.name)

    return render(request, 'main/index.html', {'title_categories' : title_categories})

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

def category(request, slug = ''):

    arr = Category.objects.filter(slug = slug)

    if arr:
        cat_id = arr[0].id

        def get_products(cat_id, result = Product.objects.none()):
            arr = Category.objects.filter(parent_id = cat_id, show = True)
            if arr:
                for i in arr:
                    result = get_products(i.id, result)
                return result
            else:
                return result | Product.objects.filter(category_id = cat_id, show = True)
        
        products = get_products(cat_id)

        info = {'products': products}

        return render(request, 'main/category.html', info)

    else: 
        return HttpResponse("<h1>Ошибочка</h1>")

def search(request):
    q = request.GET.get('q')
    
    in_name = Product.objects.filter(name__icontains = q)
    in_description = Product.objects.filter(description__icontains = q)
    in_code = Product.objects.filter(code__icontains = q)

    products = in_name | in_description | in_code

    if products:
        info = {'products' : products, 'q': q}

        return render(request, 'main/search.html', info)
    else:
        return render(request, 'main/badsearch.html', {'q': q})

def product(request, number = 0):
    product = Product.objects.filter(code = number).first()

    if product:
        info = {'product': product}

        return render(request, 'main/product.html', info)

    else:
        return HttpResponse("<h1>Товара не существует</h1>")

def getcode(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        user, _ = CustomUser.objects.get_or_create(phone=phone)

        generated_code = create_code()

        #отправляем куда-то

        user.code = generated_code
        user.save()

        return HttpResponseRedirect(reverse('test'))
        # return HttpResponse(f"<h1>{generated_code}</h1>")

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
    if request.method == 'POST':
        logout_user(request)
        return HttpResponseRedirect(reverse('main'))

def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if hasattr(request.user, 'cart'):
                code = int(request.POST.get('code', False))
                size = request.POST.get('size', False)
                color_number = int(request.POST.get('color', False))
                amount = int(request.POST.get('amount', False))

                product = Product.objects.filter(code=code).first()
                if product:
                    variation = Amount.objects.filter(product_id=product.pk, size=size, color=product.colors[color_number]).first()
                    if variation:
                        request.user.add_to_cart(variation, amount)

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main')))
            else:
                return HttpResponse(f'<h1>Админам вход запрещен</h1>')
        else:
            #модальное окно авторизации
            return HttpResponse(f'<h1>Надо зарегацца!</h1>')
        # if request.user:
        #     return HttpResponse(f'<h1>Не надо зарегацца!{request.user}</h1>')
        # else:
        #     return HttpResponse(f'<h1>Надо зарегацца!</h1>')

# def delete_from_cart(request):
#     if request.method == 'POST':
#         if 

def add_to_favorite(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if hasattr(request.user, 'cart'):
                request.user

def order(request):
    return render(request, 'main/order.html')