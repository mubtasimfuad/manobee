from .models import Cart, CartItem, Category
from .views import _skey


def categories(request):
    return {
        'categories': Category.objects.all()
    }



    
def cart_count(request):
    cart_count = 0

    if "admin" in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(skey=_skey(request))
            cartitems = CartItem.objects.filter(cart=cart)
            for cartitem in cartitems:
                cart_count+=cartitem.quantity
            
        except:
            cart_count = 0
        response = {"cart_count": cart_count}

        return response

