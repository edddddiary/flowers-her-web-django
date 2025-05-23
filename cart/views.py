from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.http import HttpResponse
# Create your views here.
def _add_cart_session_key(request):
    cart = request.session.session_key 
    if not cart:
        cart= request.session.create()
    return cart
def add_cart(request, product_id):
    product = Product.objects.get(id= product_id)
    variation_product =[]
    if request.method =="POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact = value)
                variation_product.append(variation)
            except:
                pass
    

    try:
        cart = Cart.objects.get(cart_id =_add_cart_session_key(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _add_cart_session_key(request),

        )
    cart.save()
    is_cart_item_exist= CartItem.objects.filter(product=product, cart=cart)
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product= product, cart= cart)
        ex_var_list=[]
        id =[]
        for item in cart_item:
            existing_variation = item.variation_product.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        
        if variation_product in ex_var_list:
            idex = ex_var_list.index(variation_product)
            item_id = id[idex]
            item = CartItem.objects.get(product= product, id=item_id)
            item.cart_quantity+=1 
            item.save()
        else:
            item = CartItem.objects.create(
            product = product,
            cart_quantity = 1,
            cart = cart,
            )
            if len(variation_product)>0:
                item.variation_product.clear()
                item.variation_product.add(*variation_product)
            item.save()
    else:
        
        cart_item = CartItem.objects.create(
            product = product,
            cart_quantity = 1,
            cart = cart,
        )
        if len(variation_product)>0:
            cart_item.variation_product.clear()
            cart_item.variation_product.add(*variation_product)
        cart_item.save()
    return redirect("cart:index")
def decrement(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _add_cart_session_key(request))
    product = get_object_or_404(Product, id= product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart = cart, id=cart_item_id)
        if cart_item.cart_quantity > 1:
            cart_item.cart_quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("cart:index")
    
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _add_cart_session_key(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = CartItem.objects.get(product=product, cart = cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart:index")

def increment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variation_product = []

    if request.method == "POST":
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                variation_product.append(variation)
            except Variation.DoesNotExist:
                continue

    cart = Cart.objects.get(cart_id=_add_cart_session_key(request))

    # Ambil semua cart item dengan produk dan keranjang yang sama
    cart_items = CartItem.objects.filter(product=product, cart=cart)

    for item in cart_items:
        existing_variations = item.variation_product.all()
        if list(existing_variations) == variation_product:
            # Variasi cocok → tambahkan quantity
            if item.cart_quantity < product.stock:
                item.cart_quantity += 1
                item.save()
            break
    else:
        # Tidak ada item dengan variasi yang sama → buat baru
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            cart_quantity=1
        )
        if variation_product:
            cart_item.variation_product.set(variation_product)
        cart_item.save()
    return redirect("cart:index")

def index(request, total =0, quantity =0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_add_cart_session_key(request))
    except Cart.DoesNotExist:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            cart = None

    if cart:
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.cart_quantity
            quantity += cart_item.cart_quantity

    tax = total*0.1
    real_total = total+tax
    context ={
        "products" : cart_items,
        "total" : total, 
        "quantity" : quantity,
        "tax" : tax,
        "real_total" : real_total,
    }
    return render(request, "cart/cart.html", context)