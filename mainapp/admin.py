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
