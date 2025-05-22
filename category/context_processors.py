from .models import Category
def menu_category(request):
    links = Category.objects.all()
    return dict(links=links )