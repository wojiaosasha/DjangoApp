from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('category_list', views.category_list),
    # path('category_list/<slug:slug>', views.category),
]