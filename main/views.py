from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Product

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

# def index(request):
#     return HttpResponse("<h1>Hi bitches</h1>")

def category_list(request): #ненужная хрень
    cat = Category.objects.filter(show = True)
    
    return render(request, 'main/categories.html', {'cat': cat})

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
        return HttpResponse("<h1>Ошибочка</h1>")

def product(request, number = 0):
    arr = Product.objects.filter(code = number)

    if arr:
        product = arr[0]

        info = {'product': product}

        return render(request, 'main/product.html', info)

    else:
        return HttpResponse("<h1>Товара не существует</h1>")