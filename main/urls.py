from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #главная
    path('category_list', views.category_list), #убрать
    path('catalog', views.catalog),
    path('category/<slug:slug>', views.category),
    path('search', views.search),
    path('product/<int:number>', views.product),

    # path('category_list/<slug:slug>', views.category),
]