from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from catalog.forms import CartAddProductForm
from catalog.models import Category, Product
from catalog.services.cart import Cart


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        "category": category,
        "categories": categories,
        "products": products,
    }
    return render(request, "catalog/product_list.html", context=context)


def product_detail(request, pk, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
    form = CartAddProductForm()
    context = {"categories": categories, "product": product, "cart_product_form": form}
    return render(request, "catalog/product_detail.html", context=context)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id, available=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(product, form.cleaned_data["quantity"], form.cleaned_data["override"])

    if form.cleaned_data["redirect_url"]:
        return redirect(form.cleaned_data["redirect_url"])
    return redirect("catalog:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id, available=True)
    cart.remove(product)
    return redirect("catalog:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    context = {"cart": cart}
    return render(request, "catalog/cart_detail.html", context=context)
