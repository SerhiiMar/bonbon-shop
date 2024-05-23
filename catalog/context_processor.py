from catalog.services.anonymous_cart import AnonymousCart


def cart(request):
    return {"cart": AnonymousCart(request)}
