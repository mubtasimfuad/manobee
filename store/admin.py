from turtle import color
from django.contrib import admin
import admin_thumbnails

# Register your models here.
from .models import Cart, CartItem, Category, Product, ProductVariation

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug','image')

@admin_thumbnails.thumbnail('image')
class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    
    extra= 1
@admin_thumbnails.thumbnail('image')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug','image', 'is_available', 'created_at','category','color')
    inlines = [ProductVariationInline]

    def color(self,obj):
        return obj.variations


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('skey', 'date_added',"total_price")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product_variation', 'cart', 'quantity', 'is_active', 'sub_total')

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product','color','size','stock')
    class Meta:
       
         help_texts = {
            'color': ('Leave blank to autogenerate'),
        }
        





