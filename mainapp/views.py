from django.shortcuts import render

from .models import Banner, StationeryImage, RightSectionImage, TrendingImage, Testimonial
from .models import TeamMember

def home(request):
    banner = Banner.objects.first()
    stationery_images = StationeryImage.objects.all()[:3]   # only 3
    right_section_image = RightSectionImage.objects.first()
    trending_images = TrendingImage.objects.all()[:6]       # only 6
    testimonial = Testimonial.objects.first()
    team_members = TeamMember.objects.all()

    context = {
        'banner': banner,
        'stationery_images': stationery_images,
        'right_section_image': right_section_image,
        'trending_images': trending_images,
        'testimonial': testimonial,
        'team_members': team_members,
    }
    return render(request, 'home.html', context)




from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def shop(request, slug=None):
    categories = Category.objects.all().order_by("id")

    # Default = "Office Basics", else first category
    default_cat = Category.objects.filter(name__iexact="Office Basics").first() or categories.first()

    query = request.GET.get("q", "").strip()
    if query:
        try:
            selected_category = Category.objects.get(name__iexact=query)
        except Category.DoesNotExist:
            selected_category = None
        products_qs = Product.objects.filter(category=selected_category) if selected_category else Product.objects.none()
    else:
        selected_category = get_object_or_404(Category, slug=slug) if slug else default_cat
        products_qs = Product.objects.filter(category=selected_category)

    # price filter: ?price=50-100&price=100-200 ...
    selected_ranges = request.GET.getlist("price")
    if selected_ranges:
        price_q = Q()
        for pr in selected_ranges:
            try:
                lo, hi = [int(x) for x in pr.split("-")]
                price_q |= Q(price_single__gte=lo, price_single__lte=hi)
            except Exception:
                continue
        if price_q:
            products_qs = products_qs.filter(price_q)

    total_count = products_qs.count()
    start_index = 1
    end_index = total_count

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "products": products_qs,
        "total_count": total_count,
        "start_index": start_index,
        "end_index": end_index,
        "selected_ranges": selected_ranges,
        "query": query,
    }
    return render(request, "shop.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by("id")

    # Decide which offer line to show (only one)
    offer_text = None
    if product.price_pack10:
        offer_text = f"Buy a pack of 10 @ Rs. {product.price_pack10:.2f}".rstrip("0").rstrip(".")
    elif product.price_3plus:
        offer_text = f"Buy 3 or more @ Rs. {product.price_3plus:.2f}".rstrip("0").rstrip(".")

    context = {
        "product": product,
        "reviews": reviews,
        "offer_text": offer_text,
    }
    return render(request, "product_detail.html", context)





from .models import AboutPage, AboutGallery, SectionImage

def about(request):
    banner = AboutPage.objects.first()
    gallery_images = AboutGallery.objects.all()[:3]
    pen_image = SectionImage.objects.filter(section="pen").first()
    bag_image = SectionImage.objects.filter(section="bag").first()
    stationery_image = SectionImage.objects.filter(section="stationery").first()
    team_members = TeamMember.objects.all()


    context = {
        "banner": banner,
        "gallery_images": gallery_images,
        "pen_image": pen_image,
        "bag_image": bag_image,
        "stationery_image": stationery_image,
        'team_members': team_members,
    }
    return render(request, "about.html", context)


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import ContactPage
from .forms import ContactForm

def contact(request):
    banners = ContactPage.objects.first()
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]

            subject = f"New Contact Message from {name}"
            body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"

            send_mail(
                subject,
                body,
                email,  # from user
                ["ranjitha13cs@gmail.com"],  # replace with admin email
                fail_silently=False,
            )

            messages.success(request, "Thanks for messaging, we will reach you soon.")
            return redirect("contact")

    return render(request, "contact.html", {"banners": banners, "form": form})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # home page after success
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User.objects.create_user(username=name, email=email, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html', {'banner': {"image": {"url": "/media/banner.jpg"}}})  # replace with admin upload


def my_order(request):
    return render(request, 'my_order.html')

def track_order(request):
    return render(request, 'track_order.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product, Cart, CartItem, Order, OrderItem


# ---------------- HELPER ----------------
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# ---------------- CART ----------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        return redirect("login")

    cart = get_user_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")


@login_required
def cart_view(request):
    cart = get_user_cart(request.user)
    items = cart.items.all()
    total = cart.subtotal()  # recommended to define this in Cart model

    return render(request, "cart.html", {
        "cart": cart,
        "items": items,
        "total": total,
    })

from django.http import JsonResponse
@login_required
def update_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart  # keep reference

        action = request.POST.get("action")
        if action == "inc":
            cart_item.quantity += 1
        elif action == "dec":
            cart_item.quantity -= 1
        else:
            qty = int(request.POST.get("quantity", cart_item.quantity))
            cart_item.quantity = max(qty, 0)

        if cart_item.quantity <= 0:
            cart_item.delete()
            quantity = 0
            item_total = 0
        else:
            cart_item.save()
            quantity = cart_item.quantity
            item_total = cart_item.total_price   # no ()

        return JsonResponse({
            "success": True,
            "quantity": quantity,
            "item_total": item_total,
            "subtotal": cart.subtotal(),
        })
    


from django.http import JsonResponse

@login_required
def remove_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()

        cart = get_user_cart(request.user)
        return JsonResponse({
            "success": True,
            "subtotal": cart.subtotal(),
        })



# ---------------- CHECKOUT / ORDER ----------------


from django.http import JsonResponse
from django.urls import reverse


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.all() if cart else []
    subtotal = sum([item.total_price for item in items]) if items else 0  # no ()

    if request.method == "POST":
        if not items:
            return JsonResponse({"success": False, "errors": {"cart": "Cart is empty"}})

        name = request.POST.get("name")
        street_address = request.POST.get("street_address")
        town_city = request.POST.get("town_city")
        postal_code = request.POST.get("postal_code")

        order = Order.objects.create(
            user=request.user,
            created_at=timezone.now(),
            status="pending",
            name=name,
            street_address=street_address,
            town_city=town_city,
            postal_code=postal_code,
            subtotal=subtotal,
            total=subtotal,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                unit_price=item.product.price_single,
                quantity=item.quantity,
                total_price=item.total_price,
            )

        cart.items.all().delete()

        return JsonResponse({
            "success": True,
            "redirect": reverse("order_success", args=[order.id]),
        })

    return render(request, "checkout.html", {
        "items": items,
        "subtotal": subtotal,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "home.html", {"order": order})
