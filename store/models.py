from django.db import models
from category.models import Category
# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=255, unique=True)
    slug            = models.SlugField(max_length=255, unique=True)
    description     = models.TextField(blank=True)
    stock           = models.IntegerField()
    price           = models.IntegerField()
    image           = models.ImageField(upload_to="photos/products")
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now = True )

    def __str__(self):
        return self.product_name
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category="color", is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size", is_active=True)
variation_choices=(
    ("color", "color"),
    ("size","size"),
)
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variasi_yang_sama")
    variation_category = models.CharField(max_length=50, choices=variation_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date= models.DateTimeField(auto_now_add=True)

    objects= VariationManager()

    def __str__(self):
        return self.variation_value
