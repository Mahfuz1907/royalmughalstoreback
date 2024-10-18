from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order

# Customize the Product admin to display the image from the URL
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag', 'category', 'created_at')  # Show image, name, price, etc.

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />'.format(obj.image))
        return 'No Image'
    
    image_tag.short_description = 'Image'  # Column name in admin panel

# Register your models
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)  # Register Product with the customized admin class
admin.site.register(Order)
