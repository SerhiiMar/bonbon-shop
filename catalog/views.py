from django.shortcuts import render, get_object_or_404


from catalog.models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {"category": category, "categories": categories, "products": products}
    return render(request, "catalog/product_list.html", context=context)


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context=context)
