from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpResponseRedirect
from .models import Cart, CartItem, Category, Product, ProductVariation
from django.db.models import Sum, Q
from django.contrib import messages

from django.core.paginator import  Paginator


def _skey(request):
    skey = request.session.session_key
    if not skey:
        skey = request.session.create()
    return skey


# Create your views here.
def get_products_category(request, slug=None):
    count_msg="All products"
    
    if slug!=None:
        category = get_object_or_404(Category,slug=slug)
        products =Product.objects.filter(is_available =True, category=category)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        count_msg = str(products.count())+" "+ "items found"

    else:
        products = Product.objects.filter(is_available =True)
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)

    # yield status
    product_qs = {
    "products": paged_product,
    "count": count_msg,
}
    return render(request, 'store/store.html', product_qs)



# Create your views here.
def get_products(request):
    products = Product.objects.filter(is_available =True)
    product_qs = {
        "products": products
    }
    return render(request, 'store/home.html', product_qs)



def get_product_details(request, cslug, pslug):
    
    product = get_object_or_404(Product, slug=pslug)
    product_variation = ProductVariation.objects.filter(product=product).filter(stock__gt=0)
    # is_in_cart = CartItem.objects.filter(product_variation_id=product_variation).filter(cart__skey=_skey(request)).exists()
    colors= list()
    sizes= list()
    
    for pv in product_variation:
        if pv.color not in colors:
            colors.append(pv.color)
        if pv.size not in sizes:
            sizes.append(pv.size)
    color_len = len(colors)
    colors1=colors[0]
    sum = product_variation.aggregate(Sum('stock'))
    product_qs = {
        "product": product,
        "colors": colors,
        "sizes":sizes,
        "stock":sum,
        "color1": colors1,
        "color_len":color_len,
        "product_variation": product_variation
    }
    return render(request, 'store/product_details.html', product_qs)

def search(request):
    count_msg="No result found 😞"
    if "query" in request.GET and request.GET['query']:
        query = request.GET["query"]
        if query:
            products = Product.objects.filter((Q(title__icontains=query) | Q(description__icontains=query)), is_available =True)
            
            paginator = Paginator(products, 1)
            page = request.GET.get('page',1)
            
            paged_product = paginator.get_page(page)
            if products.count()==0:
                count_msg="No result found 😞"
            else:
                count_msg = str(products.count())+" " +"results found"
            product_qs = {
    "products": paged_product,
    "count": count_msg,
    "query":query
}

            return render(request, 'store/store.html', product_qs)
    else:
        return HttpResponse("No such url")

'''
THIS PART IS DEDICATED TO CART FUNCTIONALITY
'''

#THIS PART IS DEDICATED TO CART FUNCTIONALITY



def delete_cart(request,product_variation_id):
    product_variation = ProductVariation.objects.get(id=product_variation_id)

    try:
        cart = Cart.objects.get(skey=_skey(request))
        cart_item = CartItem.objects.get(product_variation=product_variation, cart=cart)
        cart_item.delete()
    except:
        pass
    return redirect("get_cart_item")


def remove_cart(request, product_variation_id):
    product_variation = ProductVariation.objects.get(id=product_variation_id)

    try:
        cart = Cart.objects.get(skey=_skey(request))
        cart_item = CartItem.objects.get(product_variation=product_variation, cart=cart)
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass
    return redirect("get_cart_item")


def add_cart(request, product_id, color=None, size=None):
    if size==None and color == None:
        try:
            size = request.GET['size']
            color =  request.GET['color']
        except:
             return HttpResponseRedirect(request.META['HTTP_REFERER'])    
    else:
        size=size
        color=color
    # quit()


    product = Product.objects.get(id=product_id)
    try:
        product_variation =ProductVariation.objects.get(product=product ,color=color, size=size)
    except ProductVariation.DoesNotExist:
           messages.success(request, 'No Stock for the selected color and size combination. Please cosider changing color/size')
           return HttpResponseRedirect(request.META['HTTP_REFERER'])




    try:
        cart = Cart.objects.get(skey=_skey(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            skey = _skey(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product_variation=product_variation, cart=cart)
        cart_item.quantity +=1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product_variation = product_variation,
            quantity =1,
            cart = cart
        )
        cart_item.save()
    messages.success(request, 'Added to the cart')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def get_cart_item(request):
    cart_items=None
    total_price=0
    grand_total=0
    tax=0

    try:
        skey = _skey(request)
        cart = Cart.objects.get(skey=skey)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price =0
        for cartitem in cart_items:
            total_price+=cartitem.sub_total
        tax = (total_price*2)/100
        grand_total = total_price+tax
    except:
        pass

    response={
        "cart_items":cart_items,
        "total_price":total_price,
        "grand_total":grand_total,
        "tax":tax
    }
    return render(request,"store/cart.html",response)

