from django.contrib import admin
from .models import Product, Variation

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={
        "slug":("product_name",),
    }
    list_display =(
        "product_name",
        "price",
        "stock",
        "category", 
        "created_date", 
        "modified_date", 
        "is_available"
    )
    readonly_fields=(
        "created_date", "modified_date"
    )
    list_filter=(
        "category",
    )
class VariationAdmin(admin.ModelAdmin):
    list_display =(
        "product",
        "variation_category",
        "variation_value",
        "is_active",
    )
    readonly_fields=(
        "created_date",
    )
    list_editable=(
        "is_active",
    )
    list_filter=(
        "product",
        "variation_category",
        "variation_value",
    )
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)