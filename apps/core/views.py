from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from decimal import Decimal, InvalidOperation

# --- DITO ILALAGAY ANG DATA MO ---
RESTAURANT_LIST_DATA = [
    # ... (I-paste mo lahat ng data mo dito mula kay Jollibee hanggang RS) ...
]

# --- SAMPLE DATA PARA SA TOP RATED ---
TOP_RATED_DATA = [
    {'name': 'Jollibee', 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80', 'reviews': 120},
    {'name': 'Mang Inasal (CityMall)', 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80', 'reviews': 95},
    {'name': 'Kalamay Artisan Patisserie & Cafe', 'rating': 4.7, 'image': 'https://th.bing.com/th/id/OIP.Ly_7Z5aIAM0qNIUagX_JLAHaE8?r=0&pid=CanonicalCanvas', 'reviews': 85},
    {'name': 'Amore Mio Pizza & Inasal', 'rating': 4.6, 'image': 'https://th.bing.com/th/id/OIP.xjw55CL1DD1fxRTe8L42QAHaHa?r=0&pid=CanonicalCanvas', 'reviews': 75},
]

# --- SAMPLE DATA PARA SA PROMOS ---
PROMOS_DATA = [
    {'title': '50% Off First Order', 'code': 'WELCOME50', 'description': 'Valid for new users only. Max discount of ₱100.', 'color': '#eb78bf'},
    {'title': 'Free Delivery', 'code': 'FREEDEL', 'description': 'On orders above ₱500. Valid on weekends.', 'color': '#06b6d4'},
    {'title': 'Buy 1 Take 1', 'code': 'B1T1', 'description': 'On selected Chickenjoy meals. Valid until Oct 31.', 'color': '#f59e0b'},
    {'title': '₱50 Off', 'code': 'SAVE50', 'description': 'Minimum order of ₱300. Valid for all users.', 'color': '#10b981'},
]

def home(request):
    return render(request, 'admin/index.html') 

# --- BAGONG LOGIN VIEW (NAA NA ANG AUTHENTICATE) ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Kung naa ang ?next= sa URL, mobalik didto
            next_url = request.GET.get('next', '/home/')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'auth/login.html') 

def logout_view(request):
    logout(request)
    return redirect('core:login')

def near_me_view(request):
    context = {'restaurants': RESTAURANT_LIST_DATA}
    return render(request, 'admin/near_me.html', context)

def top_rated_view(request):
    context = {'top_rated': TOP_RATED_DATA}
    return render(request, 'admin/top_rated.html', context)

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    if not orders.exists():
        sample_order = {
            'id': 'SAMPLE-001',
            'restaurant_name': 'Jollibee',
            'items': 'Chickenjoy (1pc), Jolly Spaghetti',
            'total_price': 145.00,
            'status': 'Delivered',
            'created_at': 'Oct 28, 2026 • 12:30 PM'
        }
        context = {'orders': orders, 'sample_order': sample_order}
    else:
        context = {'orders': orders}
    
    return render(request, 'admin/my_orders.html', context)

def promos_view(request):
    context = {'promos': PROMOS_DATA}
    return render(request, 'admin/promos.html', context)

def restaurant_detail_view(request, rest_id):
    selected_restaurant = None
    for rest in RESTAURANT_LIST_DATA:
        if str(rest['id']) == str(rest_id):
            selected_restaurant = rest
            break
    if not selected_restaurant:
        return redirect('core:near_me')
    context = {'restaurant': selected_restaurant}
    return render(request, 'admin/restaurant_detail.html', context)

@login_required
def place_order(request, rest_id):
    if request.method == 'POST':
        items = request.POST.get('items', '').strip()
        total_price = request.POST.get('total_price', '').strip()
        
        if not total_price:
            total_price = '0.00'
        
        try:
            total_price_decimal = Decimal(total_price)
        except (InvalidOperation, TypeError, ValueError):
            total_price_decimal = Decimal('0.00')
        
        rest_name = "Unknown Restaurant"
        for rest in RESTAURANT_LIST_DATA:
            if str(rest['id']) == str(rest_id):
                rest_name = rest['name']
                break
        
        Order.objects.create(
            user=request.user,
            restaurant_name=rest_name,
            items=items,
            total_price=total_price_decimal,
            status='Pending'
        )
        return redirect('core:my_orders')
    return redirect('core:near_me')