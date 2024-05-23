import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from catalog.models import Product, Category, Cart, CartItem


TEST_DATA = {
    "user1": {
        "username": "user1_username",
        "email": "user1@test.com",
        "password": "test12password",
        "city": "user1_city",
    },
    "category1": {
        "name": "category1_name",
    },
    "product1": {
        "name": "product1_name",
        "slug": "product1-slug",
        "description": "description",
        "price": 10,
    },
    "cart_item1": {
        "price": 10,
    }
}


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            **TEST_DATA["user1"]
        )

    def setUp(self):
        self.user = get_user_model().objects.first()

    def test_user_is_abstractuser_instance(self):
        self.assertTrue(isinstance(self.user, AbstractUser))

    def test_object_name_is_username_and_full_name_in_brackets(self):
        expected_object_name = (
            f"{self.user.username} "
            f"({self.user.first_name} {self.user.last_name})"
        )
        self.assertEqual(str(self.user), expected_object_name)


class ProductModelTests(TestCase):
    @classmethod
    @freeze_time("2024-01-25")
    def setUpTestData(cls):
        category = Category.objects.create(
            **TEST_DATA["category1"]
        )
        cls.product = Product.objects.create(
            **TEST_DATA["product1"],
            category=category
        )

    def test_product_ordering_by_name_field(self):
        ordering = self.product._meta.ordering
        expected_ordering = ["name", ]
        self.assertEqual(ordering[0], expected_ordering[0])

    def test_product_creation_time_field(self):
        expected_time = datetime.datetime(2024, 1, 25, tzinfo=datetime.timezone.utc)
        actual_time = self.product.created
        self.assertEqual(actual_time, expected_time)

    @freeze_time("2024-01-26")
    def test_product_updated_time_field(self):
        expected_time = datetime.datetime(2024, 1, 26, tzinfo=datetime.timezone.utc)
        self.product.save()
        actual_time = self.product.updated
        self.assertEqual(actual_time, expected_time)

    def test_product_get_absolute_url(self):
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse(
                "catalog:product_detail",
                args=[self.product.pk, self.product.slug]
            ),
        )


class CartModelsTests(TestCase):
    @classmethod
    @freeze_time("2024-01-25")
    def setUpTestData(cls):
        cls.cart = Cart.objects.create()
        cls.product = Product.objects.create(
            **TEST_DATA["product1"],
            category=Category.objects.create(**TEST_DATA["category1"])
        )
        cls.cart_item = CartItem.objects.create(
            **TEST_DATA["cart_item1"],
            cart=cls.cart,
            product=cls.product,
        )
        print(cls.cart.items.all())

    def test_cart_ordering_by_reversed_created_field(self):
        ordering = self.cart._meta.ordering
        expected_ordering = ["-created", ]
        self.assertEqual(ordering[0], expected_ordering[0])

    def test_cart_creation_time_field(self):
        expected_time = datetime.datetime(2024, 1, 25, tzinfo=datetime.timezone.utc)
        actual_time = self.cart.created
        self.assertEqual(actual_time, expected_time)

    @freeze_time("2024-01-26")
    def test_cart_updated_time_field(self):
        expected_time = datetime.datetime(2024, 1, 26, tzinfo=datetime.timezone.utc)
        self.cart.save()
        actual_time = self.cart.updated
        self.assertEqual(actual_time, expected_time)

    def test_cart_get_total_cost(self):
        expected_sum = sum(item.price * item.quantity for item in self.cart.items.all())
        self.assertEqual(self.cart.get_total_cost(), expected_sum)

    def test_cart_item_get_cost(self):
        expected_cost = self.cart_item.price * self.cart_item.quantity
        self.assertEqual(self.cart_item.get_cost(), expected_cost)
