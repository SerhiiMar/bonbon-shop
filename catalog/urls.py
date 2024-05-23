from django.urls import path

from catalog import views


app_name = "catalog"

urlpatterns = [
    path("catalog/", views.product_list, name="product_list"),
    path("catalog/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("catalog/<int:pk>/<slug:slug>/", views.product_detail, name="product_detail"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.UserCreateView.as_view(), name="register"),

    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>", views.cart_add, name="cart-add"),
    path("cart/remove/<int:product_id>", views.cart_remove, name="cart-remove"),
]
