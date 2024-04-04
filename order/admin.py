from django.contrib import admin
from . import models

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields =['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('status', 'created_at', 'first_name', 'last_name', 'email')
    inlines = [OrderItemInline]


# Customizing the OrderItem admin display
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'get_total_price', 'quantity')

    def get_total_price(self, obj):
        return obj.price / 100

    get_total_price.short_description = 'Total Price (cents/100)'


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'created_at')

admin.site.register(models.ContactUs, ContactUsAdmin)

# Register your models here.
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)