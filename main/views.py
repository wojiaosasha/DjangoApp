from django.shortcuts import render
from django.http import HttpResponse
from .models import Category

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

# def index(request):
#     return HttpResponse("<h1>Hi bitches</h1>")

def category_list(request):
    cat = Category.objects.filter(show = True)
    
    return render(request, 'main/categories.html', {'cat': cat})

# def category(request, slug = ''):
#     cat_id = Category.objects.filter(slug = slug)[0]
#     cat = Subcategory.objects.filter(category_id = cat_id, show = True)

#     return render(request, 'main/categories.html', {'cat': cat})