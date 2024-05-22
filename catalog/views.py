from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from catalog.forms import CartAddProductForm, LoginForm, RegistrationForm
from catalog.models import Category, Product, Cart
from catalog.services.anonymous_cart import AnonymousCart


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


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect("catalog:product_list")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print("is valid")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.error(request, "Invalid login or password")

                return redirect("catalog:login")

            login(request, user)
            print(request.session.get("cart"))
            # request.session["cart"]
            return redirect("catalog:product_list")
        else:
            print("not valid")
            return render(request, "accounts/login.html", {"form": form})

    form = LoginForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("catalog:product_list")


class UserCreateView(generic.CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("catalog:login")


@require_POST
def cart_add(request, product_id):
    cart = AnonymousCart(request)
    product = get_object_or_404(Product, pk=product_id, available=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(product, form.cleaned_data["quantity"], form.cleaned_data["override"])

    if form.cleaned_data["redirect_url"]:
        return redirect(form.cleaned_data["redirect_url"])
    return redirect("catalog:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = AnonymousCart(request)
    product = get_object_or_404(Product, pk=product_id, available=True)
    cart.remove(product)
    return redirect("catalog:cart_detail")


def cart_detail(request):
    cart = AnonymousCart(request)
    context = {"cart": cart}
    return render(request, "catalog/cart_detail.html", context=context)
