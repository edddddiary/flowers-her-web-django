from django.urls import path 
from . import views 

app_name='store'

urlpatterns = [
    path("search/", views.search, name="search"),
    path("<slug:category_id>/<slug:product_id>/", views.product_detail, name="product_detail"),
    path("<slug:category_id>/", views.index, name="category"),
    path("", views.index, name="index"),
]
