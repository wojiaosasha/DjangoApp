from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'), #главная
    path('infopage/<slug:slug>', views.infopage, name='infopage'),
    path('catalog', views.catalog, name='catalog'),
    path('category/<slug:slug>', views.category, name='category'),
    path('search', views.search, name='search'),
    path('product/<int:number>', views.product, name='product'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('getcode', views.getcode, name='getcode'),
    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    path('favorite', views.favorite, name='favorite'),
    # path('<slug:slug>', views.notfound, name='notfound'), #переопределить стандарт 404
    path('api/catalog', views.api_catalog, name='api_catalog')
]