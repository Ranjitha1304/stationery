from .models import Cart

def cart_badge(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {"cart_item_count": cart.total_quantity()}
    return {"cart_item_count": 0}
