from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from catalog.utils import product_directory_path


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_list_by_category", args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    image = models.ImageField(upload_to=product_directory_path, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.pk, self.slug])


class User(AbstractUser):
    city = models.CharField(max_length=100)
    cart = models.OneToOneField("Cart", on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, through="OrderItem", related_name="orders")

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.pk

    def get_cost(self):
        return self.price * self.quantity


class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, through="CartItem", related_name="carts")

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def get_cost(self):
        return self.price * self.quantity
