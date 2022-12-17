from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'), #главная
    path('infopage/<slug:slug>', views.infopage, name='infopage'),
    path('catalog', views.catalog, name='catalog'),
    path('category/<slug:slug>', views.category, name='category'),
    path('search', views.search, name='search'),
    path('product/<int:number>', views.product),
    path('login', views.login, name='login'),
    path('logout', views.logout),
    path('getcode', views.getcode),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('order', views.order, name='order'),

    path('test', views.test_url, name='test'),
    # path('category_list/<slug:slug>', views.category),
]