from django.db import models
from django.contrib.auth.models import User

# --- AGRIHUB SPECIFIC CHOICES ---
UNIT_CHOICES = (
    ('KG', 'Kilogram'),
    ('CRATE', 'Crate/Box'),
    ('BAG', 'Bag (e.g., 50kg)'),
    ('LITER', 'Liter'),
    ('PIECE', 'Piece/Unit'),
)

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


# --- MODELS ---

class Address(models.Model):
    # Stores user delivery location.
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location / Area")
    city = models.CharField(max_length=150, verbose_name="City / Town")
    state = models.CharField(max_length=150, verbose_name="County")

    def __str__(self):
        return self.locality


class Category(models.Model):
    # Renamed to Crop Type Category
    title = models.CharField(max_length=50, verbose_name="Crop Type Title")
    slug = models.SlugField(max_length=55, verbose_name="Crop Type Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Crop Types'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Product(models.Model):
    # RENAME: Product -> Produce Item
    title = models.CharField(max_length=150, verbose_name="Produce Item Title")
    slug = models.SlugField(max_length=160, verbose_name="Produce Slug")

    # RENAME: sku -> batch_id (Preserving data with db_column='sku')
    batch_id = models.CharField(max_length=255, unique=True, verbose_name="Batch/Lot ID (SKU)", db_column='sku')

    # RENAME: short_description -> origin (Preserving data with db_column='short_description')
    origin = models.TextField(verbose_name="Origin / Short Description", db_column='short_description')

    # RENAME: detail_description -> produce_details (Preserving data with db_column='detail_description')
    produce_details = models.TextField(blank=True, null=True, verbose_name="Farming & Produce Details",
                                     db_column='detail_description')

    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Produce Image")

    # RENAME: price -> price_per_unit (Preserving data with db_column='price')
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price Per Unit/KG",
                                          db_column='price')

    # NEW FIELD: Unit Type for agricultural context
    unit_type = models.CharField(max_length=10, choices=UNIT_CHOICES, default='KG', verbose_name="Unit Type")

    # NEW FIELD: Harvest Date (critical for freshness)
    harvest_date = models.DateField(null=True, blank=True, verbose_name="Harvest Date")

    category = models.ForeignKey(Category, verbose_name="Crop Type", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Produce Items'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Cart(models.Model):
    # Tracks items added to the basket.
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Produce Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)

    # Property updated to use the new field name
    @property
    def total_price(self):
        return self.quantity * self.product.price_per_unit


class Order(models.Model):
    # Stores user orders.
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Delivery Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Produce Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
    )
    
class Inquiry(models.Model):
    # Model to capture data from the Contact Form (CRUD: Create)
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    subject = models.CharField(max_length=200, verbose_name="Inquiry Subject")
    message = models.TextField(verbose_name="Detailed Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Date")

    class Meta:
        verbose_name_plural = 'Customer Inquiries'
        ordering = ('-created_at',)

    def __str__(self):
        return self.subject + ' (' + self.name + ')'