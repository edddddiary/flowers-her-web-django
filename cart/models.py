from django.db import models
from store.models import Product, Variation
# Create your models here.
class Cart(models.Model):
    cart_id         = models.CharField(max_length=250, blank=True)
    date_added      = models.DateField(auto_now_add=True)

    def __srt__(self):
        return self.cart_id

# isi di dalam keranjang itu sendiri
class CartItem(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cart_quantity   = models.IntegerField()
    is_active       = models.BooleanField(default=True)
    variation_product = models.ManyToManyField(Variation, blank=True)

    def __str__(self):
        return self.product.product_name
    
    def total(self):
        return (self.cart_quantity* self.product.price)