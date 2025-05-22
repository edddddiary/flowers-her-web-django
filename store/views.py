from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.views import _add_cart_session_key
from cart.models import Cart, CartItem
from django.db.models import Q
# Create your views here.
def index(request, category_id = None):
    categories = None 
    products = None
    if category_id is not None:
        categories = get_object_or_404(Category,slug= category_id)
        products = Product.objects.all().filter(category=categories, is_available = True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        product_count = products.count()
    context ={
        "products" : products,
        "jumlah" : product_count,
    }
    return render(request, "store/store.html", context)

def product_detail(request, category_id, product_id):
    try:
        single_product =Product.objects.get(category__slug= category_id, slug = product_id)
        in_cart = CartItem.objects.filter(cart__cart_id=_add_cart_session_key(request), product = single_product).exists()
    except:
        raise ValueError("empty")
    context ={
        "single_product": single_product,
        "in_cart" : in_cart,
    }
    return render(request, "store/product_detail.html", context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context ={
        "products" : products,
        "jumlah" : product_count,
    }
    return render(request, "store/store.html", context)