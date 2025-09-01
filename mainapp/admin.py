from django.contrib import admin
from .models import Banner, StationeryImage, RightSectionImage, TrendingImage, Testimonial

admin.site.register(Banner)
admin.site.register(StationeryImage)
admin.site.register(RightSectionImage)
admin.site.register(TrendingImage)
admin.site.register(Testimonial)


from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price_single", "price_pack10", "price_3plus", "rating")
    list_filter = ("category", "rating")
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "title", "rating")
    list_filter = ("rating",)


from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "designation")



from .models import AboutPage, AboutGallery, SectionImage

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("id", "banner_image",)

@admin.register(AboutGallery)
class AboutGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "image",)

@admin.register(SectionImage)
class SectionImageAdmin(admin.ModelAdmin):
    list_display = ("section", "image")


from .models import ContactPage

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("id", "banner_top", "banner_bottom")


from .models import FeaturedProduct, BackToSchoolProduct

@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order')
    ordering = ('order',)

@admin.register(BackToSchoolProduct)
class BackToSchoolProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order')
    ordering = ('order',)



# admin.py
from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "created_at", "expected_delivery_date")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "user__username", "name", "street_address")
    readonly_fields = ("order_number", "created_at")
    fields = (
        "order_number", "user", "status", "created_at",
        "confirmed_at", "shipped_at", "out_for_delivery_at", "delivered_at",
        "expected_delivery_date",
        "name", "street_address", "town_city", "postal_code",
        "subtotal", "total"
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "quantity", "total_price")
    search_fields = ("product_name", "order__order_number")
