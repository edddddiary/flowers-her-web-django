from .models import Cart, CartItem
from .views import _add_cart_session_key
def jumlah(request):
    jum =0
    try:
        cart = Cart.objects.get(cart_id=_add_cart_session_key(request))
        cart_items = CartItem.objects.filter(cart= cart, is_active=True)
        for cart_item in cart_items:
            jum+= cart_item.cart_quantity
    except:
        jum=0

    return dict(jum = jum)