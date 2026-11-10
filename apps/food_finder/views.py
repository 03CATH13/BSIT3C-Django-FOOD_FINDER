from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import urllib.parse
from .forms import RestaurantForm, RegisterForm
from .models import Favorite, Restaurant
from django.contrib.auth.models import User
from apps.core.models import Order 

# ==========================================
# RESTAURANT DATA
# ==========================================
RESTAURANT_LIST_DATA = [
    # --- FAST FOOD ---
    {
        'id': 1, 'name': 'Jollibee', 'cuisine_type': 'Fast Food', 'address': 'Guanzon St/City Proper, Kabankalan City', 'opening_hours': '9AM - 9PM', 'image': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80', 'description': 'Well-known Philippines fast-food chain.', 'lat': '9.99028', 'lng': '122.81472', 'price': '₱100-₱200', 'rating': 4.5, 'menu': [{'name': 'Chickenjoy (1pc)', 'price': '₱85'}, {'name': 'Jolly Spaghetti', 'price': '₱60'}, {'name': 'Yumburger', 'price': '₱45'}, {'name': 'Chicken with Rice', 'price': '₱99'}]},
    {
        'id': 2, 'name': 'Mang Inasal (CityMall)', 'cuisine_type': 'Fast Food', 'address': 'Level 1, CityMall Kabankalan, Justice Perez Highway', 'opening_hours': '8AM - 10PM', 'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80', 'description': 'Home of the famous Chicken Inasal.', 'lat': '9.99388', 'lng': '122.81798', 'price': '₱150-₱250', 'rating': 4.8, 'menu': [{'name': 'Paborito Meal (PM1)', 'price': '₱120'}, {'name': 'Unli Rice', 'price': '₱35'}, {'name': 'Paa Large Uli Rice', 'price': '₱185'}]},
    {
        'id': 3, 'name': "McDonald's", 'cuisine_type': 'Fast Food', 'address': 'Guanzon St., Kabankalan City', 'opening_hours': 'Open 24/7', 'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500&q=80', 'description': "I'm lovin' it.", 'lat': '9.98998', 'lng': '122.81442', 'price': '₱100-₱200', 'rating': 4.3, 'menu': [{'name': 'Big Mac', 'price': '₱150'}, {'name': 'Fries (Medium)', 'price': '₱65'}, {'name': 'Chicken Mcdo large (1pc)', 'price': '₱125'}]},
    {
        'id': 4, 'name': 'Chowking', 'cuisine_type': 'Fast Food', 'address': 'City Proper, Kabankalan', 'opening_hours': 'Open Daily', 'image': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&q=80', 'description': 'Chinese-style fast food.', 'lat': '9.99058', 'lng': '122.81592', 'price': '₱100-₱200', 'rating': 4.1, 'menu': [{'name': 'Chao Fan w/ Siomai', 'price': '₱95'}, {'name': 'Beef Wanton Mami', 'price': '₱110'}]},
    
    # --- LOCAL & CANSI ---
    {
        'id': 6, 'name': "ALONSO's Cansi & Sizzling House", 'cuisine_type': 'Local & Cansi', 'address': 'Guanzon St, Brgy. 1', 'opening_hours': 'Open 24/7', 'image': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80', 'description': 'Famous Cansi and Sizzling Sisig.', 'lat': '9.99008', 'lng': '122.81652', 'price': '₱150-₱300', 'rating': 4.6, 'menu': [{'name': 'Cansi (Good for 2)', 'price': '₱180'}, {'name': 'Sizzling Sisig', 'price': '₱130'}]},
    {
        'id': 7, 'name': "Myrna's Restaurant", 'cuisine_type': 'Local & Cansi', 'address': 'Tan Lorenzo Street, Kabankalan City', 'opening_hours': '8AM - 8PM', 'image': 'https://images.unsplash.com/photo-1626776876729-bab4369a5a5a?w=500&q=80', 'description': 'Filipino home-cooked meals.', 'lat': '9.98958', 'lng': '122.81508', 'price': '₱80-₱150', 'rating': 4.2, 'menu': [{'name': 'Pork Adobo w/ Rice', 'price': '₱85'}, {'name': 'Sinigang na Baboy', 'price': '₱120'}]},
    {
        'id': 8, 'name': '3RD Talabahan', 'cuisine_type': 'Local & Cansi', 'address': 'Lirazan Street, Kabankalan City', 'opening_hours': '10AM - 10PM', 'image': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=500&q=80', 'description': 'Fresh seafood and grilled fish.', 'lat': '9.98898', 'lng': '122.81698', 'price': '₱150-₱350', 'rating': 4.7, 'menu': [{'name': 'Grilled Fish', 'price': '₱150'}, {'name': 'Buttered Shrimp', 'price': '₱200'}]},
    
    # --- CAFE & SNACKS ---
    {
        'id': 5, 'name': 'Taza La Bien', 'cuisine_type': 'Cafe & Snacks', 'address': 'Los Angeles St, Brgy. 1', 'opening_hours': '10AM - 10PM', 'image': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500&q=80', 'description': 'Coffee, pastries, and pasta.', 'lat': '9.99108', 'lng': '122.81758', 'price': '₱80-₱150', 'rating': 4.4, 'menu': [{'name': 'Iced Latte', 'price': '₱120'}, {'name': 'Wintermelon Milktea', 'price': '₱75'}]},
    {
        'id': 23, 'name': 'Chatime Kabankalan', 'cuisine_type': 'Cafe & Snacks', 'address': 'CityMall Kabankalan, Justice Perez Highway', 'opening_hours': '10AM - 9PM', 'image': 'https://images.unsplash.com/photo-1558857563-b371033873b8?w=500&q=80', 'description': 'Famous milk tea chain with various flavors.', 'lat': '9.99388', 'lng': '122.81798', 'price': '₱80-₱150', 'rating': 4.5, 'menu': [{'name': 'Pearl Milk Tea', 'price': '₱95'}, {'name': 'Matcha Latte', 'price': '₱110'}]},
    {
        'id': 24, 'name': 'Macao Imperial Tea', 'cuisine_type': 'Cafe & Snacks', 'address': 'Gaisano Grand Mall Kabankalan', 'opening_hours': '10AM - 9PM', 'image': 'https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=500&q=80', 'description': 'Premium milk tea and cheesecake series.', 'lat': '9.98758', 'lng': '122.81208', 'price': '₱80-₱150', 'rating': 4.7, 'menu': [{'name': 'Cream Cheese Milk Tea', 'price': '₱120'}, {'name': 'Taro Milktea', 'price': '₱105'}]},
    
    # --- MGA BAGONG DAGDAG (LOCAL FAVORITES) ---
    {
        'id': 20, 'name': 'Aida\'s Carinderia', 'cuisine_type': 'Local & Cansi', 'address': 'Public Market Area, Brgy. 1, Kabankalan City', 'opening_hours': '6AM - 7PM', 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80', 'description': 'Authentic home-cooked Filipino dishes and local viands.', 'lat': '9.99058', 'lng': '122.81492', 'price': '₱50-₱100', 'rating': 4.2, 'menu': [{'name': 'Pork Adobo', 'price': '₱65'}, {'name': 'Sinigang', 'price': '₱75'}, {'name': 'Fried Chicken', 'price': '₱85'}]},
    {
        'id': 21, 'name': 'Tita Beth\'s Eatery', 'cuisine_type': 'Local & Cansi', 'address': 'Guanzon St., Brgy. 2, Kabankalan City', 'opening_hours': '7AM - 8PM', 'image': 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=500&q=80', 'description': 'Comfort food and budget-friendly meals.', 'lat': '9.98998', 'lng': '122.81542', 'price': '₱50-₱100', 'rating': 4.0, 'menu': [{'name': 'Pancit Canton', 'price': '₱60'}, {'name': 'Lumpia', 'price': '₱40'}, {'name': 'Rice', 'price': '₱15'}]},
    {
        'id': 22, 'name': 'Kabankalan Ihaw-Ihaw', 'cuisine_type': 'Local & Cansi', 'address': 'Rizal St., Brgy. 3, Kabankalan City', 'opening_hours': '4PM - 12AM', 'image': 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=500&q=80', 'description': 'Best pork BBQ and grilled seafood in town.', 'lat': '9.98858', 'lng': '122.81492', 'price': '₱50-₱150', 'rating': 4.6, 'menu': [{'name': 'Pork BBQ (5 sticks)', 'price': '₱100'}, {'name': 'Grilled Squid', 'price': '₱150'}, {'name': 'Puso ng Saging', 'price': '₱25'}]},
    {
        'id': 25, 'name': 'Angel\'s Burger', 'cuisine_type': 'Fast Food', 'address': 'Lirazan St., Brgy. 4, Kabankalan City', 'opening_hours': '10AM - 8PM', 'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80', 'description': 'Famous local burger stand with homemade patties.', 'lat': '9.98708', 'lng': '122.81358', 'price': '₱50-₱100', 'rating': 4.4, 'menu': [{'name': 'Double Cheeseburger', 'price': '₱85'}, {'name': 'Bacon Burger', 'price': '₱95'}]},
    {
        'id': 26, 'name': 'Lola Nena\'s Lomi House', 'cuisine_type': 'Fast Food', 'address': 'Tan Lorenzo St., Kabankalan City', 'opening_hours': '8AM - 6PM', 'image': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500&q=80', 'description': 'The best Lomi in the city, perfect for rainy days.', 'lat': '9.98958', 'lng': '122.81508', 'price': '₱80-₱150', 'rating': 4.5, 'menu': [{'name': 'Special Lomi', 'price': '₱90'}, {'name': 'Lomi Overload', 'price': '₱120'}]},
    {
        'id': 30, 'name': 'Samgyupsalamat Kabankalan', 'cuisine_type': 'Fast Food', 'address': 'Guanzon St., Brgy. 2, Kabankalan City', 'opening_hours': '11AM - 10PM', 'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80', 'description': 'Unlimited Korean BBQ experience.', 'lat': '9.98998', 'lng': '122.81542', 'price': '₱400-₱500', 'rating': 4.8, 'menu': [{'name': 'Unlimited Pork', 'price': '₱399'}, {'name': 'Unlimited Beef', 'price': '₱499'}]}
]

# ==========================================
# DASHBOARD (BINAGO PARA MAIPASA SA HOME.HTML)
# ==========================================
@login_required
def home(request):
    total_favorites = Favorite.objects.filter(user=request.user).count()
    user_name = request.user.first_name if request.user.first_name else request.user.username
    
    # Kukunin natin ang unang 3 para sa "Trending Nearby You"
    trending_restaurants = RESTAURANT_LIST_DATA[:3]
    # Ang natitira para sa "All Restaurants" (o pwede ring lahat)
    all_restaurants = RESTAURANT_LIST_DATA
    
    context = {
        'Girlies': user_name, 
        'greeting': 'Welcome', 
        'total_restaurants': len(RESTAURANT_LIST_DATA), 
        'total_favorites': total_favorites,
        'trending_restaurants': trending_restaurants, # <-- IDINAGDAG
        'all_restaurants': all_restaurants,           # <-- IDINAGDAG
    }
    return render(request, 'home.html', context)

# ==========================================
# RESTAURANT LIST (Search at Category Filter)
# ==========================================
@login_required
def restaurant_list(request):
    restaurants = RESTAURANT_LIST_DATA.copy()
    query = request.GET.get('q', '').strip()
    cuisine_filter = request.GET.get('cuisine', '').strip()
    
    if query:
        search_text = query.casefold()
        filtered_restaurants = []
        for restaurant in restaurants:
            name = restaurant.get('name', '')
            address = restaurant.get('address', '')
            cuisine = restaurant.get('cuisine_type', '')
            description = restaurant.get('description', '')
            menu = restaurant.get('menu', [])
            matches_restaurant = (search_text in name.casefold() or search_text in address.casefold() or search_text in cuisine.casefold() or search_text in description.casefold())
            matches_menu = any(search_text in item.get('name', '').casefold() for item in menu)
            if matches_restaurant or matches_menu:
                filtered_restaurants.append(restaurant)
        restaurants = filtered_restaurants

    if cuisine_filter:
        clean_filter = cuisine_filter.lower().replace('+', ' ').replace('%26', '&').strip()
        filtered_by_cuisine = []
        for restaurant in restaurants:
            cuisine_type = restaurant.get('cuisine_type', '').lower()
            if clean_filter in cuisine_type or cuisine_type in clean_filter:
                filtered_by_cuisine.append(restaurant)
        restaurants = filtered_by_cuisine

    favorite_ids = []
    if request.user.is_authenticated:
        user_favs = Favorite.objects.filter(user=request.user).select_related('restaurant')
        favorite_ids = [fav.restaurant.id for fav in user_favs if fav.restaurant]
    total_favorites = len(favorite_ids)
    
    for restaurant in restaurants:
        restaurant['menu_items'] = restaurant.get('menu', [])
        restaurant['is_favorited'] = restaurant['id'] in favorite_ids
        
    return render(request, 'restaurant_list.html', {
        'restaurants': restaurants, 
        'restaurant_list': restaurants, 
        'query': query, 
        'current_cuisine': cuisine_filter, 
        'total_restaurants': len(restaurants), 
        'total_favorites': total_favorites
    })

# (Panatilihin ang iba pang functions sa ibaba: restaurant_detail, restaurant_map, toggle_favorite, my_favorites, info_management, add_restaurant, register_view, about_view, place_order, owner_dashboard, accept_order, mark_delivered, my_orders)

@login_required
def restaurant_detail(request, pk):
    pk = int(pk)
    restaurant = None
    for item in RESTAURANT_LIST_DATA:
        if item['id'] == pk:
            restaurant = item
            break
    if restaurant is None:
        return redirect('food_finder:restaurant_list')
    restaurant['menu_items'] = restaurant.get('menu', [])
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})

@login_required
def restaurant_map(request):
    return render(request, 'map.html', {'restaurant_list': RESTAURANT_LIST_DATA, 'restaurants': RESTAURANT_LIST_DATA})

@login_required
def add_review(request, pk):
    return redirect('food_finder:restaurant_list')

@login_required
def toggle_favorite(request, pk):
    try:
        restaurant_data = next((r for r in RESTAURANT_LIST_DATA if r['id'] == pk), None)
        if restaurant_data:
            restaurant_obj, created = Restaurant.objects.get_or_create(id=pk, defaults={'name': restaurant_data['name'], 'description': restaurant_data.get('description', ''), 'address': restaurant_data['address'], 'city': 'Kabankalan', 'cuisine_type': 'other', 'opening_hours': restaurant_data.get('opening_hours', '')})
            favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant_obj).first()
            if favorite:
                favorite.delete()
            else:
                Favorite.objects.create(user=request.user, restaurant=restaurant_obj)
    except Exception as e:
        print(f"Error in toggle_favorite: {e}")
    return redirect('food_finder:restaurant_list')

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    fav_ids = [fav.restaurant.id for fav in favorites if fav.restaurant]
    favorite_restaurants = [r for r in RESTAURANT_LIST_DATA if r['id'] in fav_ids]
    return render(request, 'my_favorites.html', {'favorites': favorite_restaurants})

@login_required
def info_management(request):
    all_users = User.objects.all().order_by('-date_joined')
    return render(request, 'info.html', {'users': all_users})

@login_required
def add_restaurant(request):
    return redirect('food_finder:restaurant_list')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('food_finder:restaurant_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def about_view(request):
    return render(request, 'about.html')

@login_required
def place_order(request, pk):
    if request.method == 'POST':
        items = request.POST.get('items')
        total_price = request.POST.get('total_price')
        restaurant_obj = get_object_or_404(Restaurant, id=pk)
        Order.objects.create(
            customer=request.user,
            restaurant=restaurant_obj,
            restaurant_name=restaurant_obj.name,
            items=items,
            total_price=total_price,
            status='Pending'
        )
        return redirect('food_finder:my_orders')
    return redirect('food_finder:restaurant_list')

@login_required
def owner_dashboard(request):
    my_restaurants = Restaurant.objects.filter(owner=request.user)
    orders = Order.objects.filter(restaurant__in=my_restaurants).order_by('-created_at')
    return render(request, 'owner_dashboard.html', {'orders': orders})

@login_required
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.restaurant.owner == request.user and request.method == 'POST':
        order.status = 'Preparing'
        order.save()
    return redirect('food_finder:owner_dashboard')

@login_required
def mark_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.restaurant.owner == request.user and request.method == 'POST':
        order.status = 'Delivered'
        order.save()
    return redirect('food_finder:owner_dashboard')

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})