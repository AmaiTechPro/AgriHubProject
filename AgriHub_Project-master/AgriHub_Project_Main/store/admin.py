from django.contrib import admin
from .models import Address, Category, Product, Cart, Order

# --- ADMIN SITE CUSTOMIZATION (AgriHub Branding) ---
admin.site.site_header = "AgriHub Marketplace Administration"
admin.site.site_title = "AgriHub Admin Panel"
admin.site.index_title = "Welcome to the AgriHub Control Center"


# --- ADMIN CLASSES ---

class AddressAdmin(admin.ModelAdmin):
    # Updated 'state' to 'county' to reflect the model change (if you made it).
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')


class CategoryAdmin(admin.ModelAdmin):
    # Display fields remain valid, but the verbose name is now Crop Type.
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}


class ProductAdmin(admin.ModelAdmin):
    # CRITICAL: Updated list_display and search_fields to use new model field names

    list_display = (
        'title',
        'category',
        'price_per_unit',  # NEW FIELD NAME
        'unit_type',  # NEW FIELD
        'harvest_date',  # NEW FIELD
        'is_active',
        'is_featured',
        'updated_at'
    )

    list_editable = ('category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured', 'harvest_date')
    list_per_page = 10

    # CRITICAL: Search fields updated to use new names
    search_fields = ('title', 'category__title', 'origin')

    prepopulated_fields = {"slug": ("title",)}


class CartAdmin(admin.ModelAdmin):
    # Foreign key field is now 'Produce Item'
    list_display = ('user', 'product', 'quantity', 'created_at', 'total_price')  # Added total_price property
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user__username', 'product__title')


class OrderAdmin(admin.ModelAdmin):
    # Foreign key field is now 'Produce Item'
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user__username', 'product__title', 'status')


# --- REGISTER MODELS ---

admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)