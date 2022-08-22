from http.client import HTTPResponse
from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('',views.get_products, name="get_products"),
    path('store/',views.get_products_category, name="get_products_category"),
    path('store/search',views.search, name="search"),

    path('store/category/<slug:slug>/',views.get_products_category, name="get_product_by_category"),
    path('store/category/<slug:cslug>/<slug:pslug>/',views.get_product_details, name="get_product_details"),

    #url patterns for cart fubctions
    path('store/cart/',views.get_cart_item, name="get_cart_item"),
    path('store/cart/add/<int:product_id>/<str:color>/<str:size>',views.add_cart, name="add_cart"),
    path('store/cart/add/<int:product_id>/',views.add_cart, name="add_cart_from_product_details"),

    path('store/cart/remove/<int:product_variation_id>',views.remove_cart, name="remove_cart"),
    path('store/cart/delete/<int:product_variation_id>',views.delete_cart, name="delete_cart"),


    







]