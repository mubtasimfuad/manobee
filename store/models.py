from email.policy import default
from itertools import product
from colorfield.fields import ColorField
from django import VERSION as DJANGO_VERSION

from django.db import models
from django.urls import reverse
from uuid import uuid4
from django.db.models import Sum
from django.core.exceptions import ValidationError
from . import pil
from django.db.models.signals import pre_save
from django.dispatch import receiver





# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("get_product_by_category", args=[self.slug])
    


class Product(models.Model):
    title    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=4000, blank=True)
    price           = models.DecimalField(max_digits=7, decimal_places=2)
    image         = models.ImageField(upload_to='photos/products', default='no.jpg')
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at    = models.DateTimeField(auto_now_add=True)
    modified_at   = models.DateTimeField(auto_now=True)
    

    
    class Meta:
        ordering = ('-modified_at',)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("get_product_details", args=[self.category.slug,self.slug])


choices=[
    ('32','32'),('34','34'),( '36', '36'),('38', '38'),('40','40'),
 ( '42', '42'),('44','44'),('46','46'), ('Default','Default')]

class ProductVariation(models.Model):
    
    product = models.ForeignKey('Product', related_name='variations', on_delete= models.CASCADE)
    image   = models.ImageField(upload_to='photos/products', null =True)
    stock   = models.PositiveIntegerField()
    added_price = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    color = ColorField(null = True)
    size = models.CharField(choices=choices, null=True, max_length=20, default='Dpy efault')
    class Meta:
        unique_together = ["product","color", "size"]

        
   
    def save(self, *args, **kwargs):
        
        if self.color is None:
            self.color = pil._get_image_field_color(self)
            super(ProductVariation, self).save(*args, **kwargs)
  

    def __str__(self):
        return self.product.title 



     
    

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    skey = models.CharField(max_length=250, null=True)
    total_price = models.PositiveIntegerField(editable=False, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.skey
   


class CartItem(models.Model):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='cartitems')
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
   
    @property
    def sub_total(self):
        return ((self.product_variation.product.price* self.quantity)+self.product_variation.added_price)
    def __unicode__(self):
        return self.product_variation.product
    def unit_price(self):
        return self.product_variation.product.price +self.product_variation.added_price
    
   
    

