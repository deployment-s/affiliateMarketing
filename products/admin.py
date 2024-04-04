from django.contrib import admin
from . import models




class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_display_price', 'get_rating')

    def get_display_price(self, obj):
        return obj.price / 100

    get_display_price.short_description = 'Price (Divided by 100)'

    def get_rating(self, obj):
        return obj.get_rating()

    get_rating.short_description = 'Rating'

admin.site.register(models.Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'rating', 'content', 'created_by', 'created_at')

admin.site.register(models.Review, ReviewAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(models.Category, CategoryAdmin)
