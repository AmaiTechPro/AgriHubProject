from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from decimal import Decimal # Required for handling Decimal field calculati
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group # Needed for Group checks
from .models import FarmerProfile # Needed for Farmer specific data



# --- AGRIHUB MODELS ---
from .models import Product, Category, Cart, Order, Address, Inquiry
from .forms import LoginForm, RegistrationForm # Placeholder imports for forms (assume they exist) 

# --- HOME & BASE VIEWS ---

def home(request):
    """Renders the homepage, displaying featured products."""
    products = Product.objects.filter(is_featured=True, is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/index.html', context)

def detail(request, slug):
    """Renders the single product detail page."""
    product = Product.objects.get(slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(slug=slug)[:4]
    context = {'product': product, 'related_products': related_products}
    return render(request, 'store/product_detail.html', context)

def all_categories(request):
    """Renders a page listing all active categories."""
    categories = Category.objects.filter(is_active=True)
    context = {'categories': categories}
    return render(request, 'store/all_categories.html', context)

def category_products(request, slug):
    """Renders products filtered by a specific category slug."""
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    context = {'category': category, 'products': products}
    return render(request, 'store/category_products.html', context)

# --- INQUIRY/CONTACT VIEWS (CRUD: CREATE) ---

def blog(request):
    """Renders the blog page."""
    return render(request, 'store/blog.html')

def contact(request):
    """Handles contact form submission and inquiry creation."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_content = request.POST.get('message')
        
        if not name or not email or not subject or not message_content:
            messages.error(request, "Error: All fields are required. Please try again.")
            return render(request, 'store/contact.html')

        try:
            Inquiry.objects.create(
                name=name, email=email, subject=subject, message=message_content
            )
            messages.success(request, "Request Received! Thank you for contacting AgriHub.")
            return redirect('store:contact')
        
        except Exception as e:
            messages.error(request, f"An error occurred while saving: {e}")
            
    return render(request, 'store/contact.html')


# --- CART/ORDER VIEWS (CORE LOGIC) ---

@login_required
def add_to_cart(request):
    """Adds a produce item to the user's cart (Basket)."""
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    
    # Check if item already exists in cart
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('/cart/') 

@login_required
def cart(request):
    """Renders the shopping cart (Order Basket) page with total calculations."""
    user = request.user
    cart_products = Cart.objects.filter(user=user)
    addresses = Address.objects.filter(user=user)
    
    amount = Decimal(0)
    for p in cart_products:
        # CRITICAL FIX: Use price_per_unit
        temp_amount = (p.quantity * p.product.price_per_unit)
        amount += temp_amount
    
    shipping_amount = Decimal(10)
    total_amount = amount + shipping_amount
    
    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': total_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)

@login_required
def remove_cart(request, cart_id):
    """Deletes an item from the cart (Basket). (CRUD: DELETE)"""
    Cart.objects.filter(id=cart_id).delete()
    return redirect('store:cart')

@login_required
def plus_cart(request, cart_id):
    """Increments the quantity of an item in the cart. (CRUD: UPDATE)"""
    c = Cart.objects.get(id=cart_id)
    c.quantity += 1
    c.save()
    return redirect('store:cart')

@login_required
def minus_cart(request, cart_id):
    """Decrements the quantity of an item in the cart. (CRUD: UPDATE)"""
    c = Cart.objects.get(id=cart_id)
    if c.quantity > 1:
        c.quantity -= 1
        c.save()
    return redirect('store:cart')


def checkout(request):
    """Renders the checkout page (Placeholder logic for now)."""
    # NOTE: This should contain the final order creation logic in a real app.
    return render(request, 'store/checkout.html')


@login_required
def orders(request):
    """Renders the user's order history."""
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'store/orders.html', context)

# --- USER/ADDRESS VIEWS ---

def profile(request):
    """Renders the user profile page."""
    # NOTE: Assuming you have forms for Profile editing and Address listing here
    addresses = Address.objects.filter(user=request.user)
    context = {'addresses': addresses}
    return render(request, 'account/profile.html', context)

class AddressView(View):
    """Handles adding a new delivery address."""
    # NOTE: Assuming AddressForm is defined elsewhere
    def get(self, request):
        return render(request, 'account/add_address.html')

    def post(self, request):
        # Placeholder for saving address form data
        return redirect('store:profile')

@login_required
def remove_address(request, id):
    """Deletes a saved address. (CRUD: DELETE)"""
    Address.objects.filter(id=id).delete()
    messages.success(request, "Delivery address removed successfully.")
    return redirect('store:profile')




# Find and REPLACE the existing RegistrationView class:

class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        is_farmer = request.POST.get('is_farmer') # Check for the new checkbox field
        
        if form.is_valid():
            # 1. Save the new Django User
            user = form.save()
            
            # 2. Check Role and Assign Group
            if is_farmer:
                # CRITICAL: Create the dedicated Farmer Profile record
                FarmerProfile.objects.create(
                    user=user,
                    farm_name=f"{user.username}'s New Farm", 
                    farm_location="Needs Update",
                    phone_number="Needs Update"
                )
                # Assign to Farmer Group (RBAC)
                farmer_group, created = Group.objects.get_or_create(name='Farmer_Seller')
                user.groups.add(farmer_group)
                messages.success(request, f"Welcome, Farmer {user.username}! Your selling profile has been created.")
            else:
                # Assign standard Consumer Group
                consumer_group, created = Group.objects.get_or_create(name='Consumer_Buyer')
                user.groups.add(consumer_group)
                messages.success(request, f"Welcome to AgriHub, {user.username}! Please log in to shop.")
                
            return redirect('store:login')
        else:
            # If invalid, re-render the page with form and errors
            messages.error(request, "Registration failed. Please correct the errors.")
            return render(request, 'account/register.html', {'form': form})



def test(request):
    """Placeholder view for testing."""
    return render(request, 'store/test.html')




# Add the Delete View (CRUD: DELETE)
@login_required
def farmer_delete_produce(request, pk):
    """Deletes a produce item (CRUD: DELETE)."""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # The actual delete operation
        product.delete()
        messages.success(request, f"Produce '{product.title}' successfully deleted.")
        return redirect('store:home') # Redirect to homepage or dashboard
        
    context = {'product': product}
    return render(request, 'store/farmer_confirm_delete.html', context)\
    


    # In store/views.py, add this function:

# In store/views.py, add this function:

@login_required
def farmer_edit_produce(request, pk):
    """Front-end view for Farmers to edit an existing produce item (CRUD: UPDATE)."""
    # 1. Ensure the product exists
    product = get_object_or_404(Product, pk=pk)
    
    # 2. Add privilege check (optional but secure: ensure the current user owns this product)
    # NOTE: This requires adding a foreign key 'farmer' to the Product model. 
    # Since we skipped that, we rely on the Admin permissions being set correctly.

    if request.method == 'POST':
        # Populate the form with the POST data and the existing product instance
        form = FarmerProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Produce '{product.title}' updated successfully.")
            return redirect('store:home') # Redirect to homepage or dashboard
        else:
            messages.error(request, "Update failed. Please correct errors.")
    else:
        # GET request: display the form pre-filled with current data
        form = FarmerProductForm(instance=product)

    context = {'form': form, 'product': product, 'editing': True}
    return render(request, 'store/farmer_add_produce.html', context)






@login_required
def add_produce_view(request):
    """Front-end view for Farmers to add a new produce item."""
    # NOTE: In a complete app, you would add a check here to ensure only 'Farmer_Seller' can access this page.
    
    if request.method == 'POST':
        # Instantiates the form with POST data and uploaded files
        # FarmerProductForm must be correctly defined in store/forms.py
        form = FarmerProductForm(request.POST, request.FILES) 
        if form.is_valid():
            # Save the product
            form.save()
            
            messages.success(request, "New produce item added successfully!")
            return redirect('store:home') # Redirect to the homepage or a dashboard
        else:
            messages.error(request, "Failed to add product. Check required fields and try again.")
    else:
        # GET request: display the blank form
        form = FarmerProductForm()

    context = {'form': form}
    return render(request, 'store/farmer_add_produce.html', context)