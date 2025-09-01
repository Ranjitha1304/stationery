from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    
    def __str__(self):
        return f"Banner {self.id}"


class StationeryImage(models.Model):
    image = models.ImageField(upload_to='stationery/')
    
    def __str__(self):
        return f"Stationery Image {self.id}"


class RightSectionImage(models.Model):
    image = models.ImageField(upload_to='right_section/')
    
    def __str__(self):
        return f"Right Section Image {self.id}"


class TrendingImage(models.Model):
    image = models.ImageField(upload_to='trending/')
    
    def __str__(self):
        return f"Trending Image {self.id}"


class Testimonial(models.Model):
    heading = models.CharField(max_length=200, default="Customer Testimonial")
    subtitle = models.CharField(max_length=200, default="Bulk Stationery. Better Prices. Smarter Supply.")
    profile_image = models.ImageField(upload_to='testimonials/')
    text = models.TextField()
    customer_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"Testimonial by {self.customer_name}"




from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    banner = models.ImageField(upload_to="categories/")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]     


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products/")
    price_single = models.DecimalField(max_digits=10, decimal_places=2)
    # Only ONE of these is required per product:
    price_pack10 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_3plus  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)  # 0..5
    one_line_heading = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    key_features = models.TextField(help_text="Enter features separated by new lines")

    def get_features_list(self):
        return [line for line in self.key_features.splitlines() if line.strip()]

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(default=0)  # 0..5
    content = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.product.name}"

    

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team/")

    def __str__(self):
        return self.name



# mainapp/models.py
from django.db import models

class AboutPage(models.Model):
    banner_image = models.ImageField(upload_to="about/banner/")

    def __str__(self):
        return "About Page Content"


class AboutGallery(models.Model):
    image = models.ImageField(upload_to="about/gallery/")

    def __str__(self):
        return f"Gallery Image {self.id}"


class SectionImage(models.Model):
    SECTION_CHOICES = [
        ("pen", "Pen & Pencil"),
        ("bag", "Bag"),
        ("stationery", "All Stationery"),
    ]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    image = models.ImageField(upload_to="about/sections/")

    def __str__(self):
        return f"{self.get_section_display()} Image"



class ContactPage(models.Model):
    banner_top = models.ImageField(upload_to="contact/banner/")
    banner_bottom = models.ImageField(upload_to="contact/banner/")

    def __str__(self):
        return "Contact Page Banners"




from django.conf import settings
from django.db import models
from django.utils import timezone


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    def total_quantity(self):
        """Total no. of items in the cart (for badge in navbar)."""
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id} ({self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def unit_price(self):
        return self.product.price_single

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )

    # Billing info
    name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=500)
    town_city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "Product", null=True, blank=True, on_delete=models.SET_NULL
    )
    product_name = models.CharField(max_length=300)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} ({self.order})"



from django.db import models

class FeaturedProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Featured: {self.product.name}"

class BackToSchoolProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Back to School: {self.product.name}"
