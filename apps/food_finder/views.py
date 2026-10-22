from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import urllib.parse


# ==========================================
# GLOBAL DATA (May Image, Menu, Lat, Lng)
# ==========================================
RESTAURANTS_DATA = [
    {
        'id': 1, 'name': 'Jollibee', 'cuisine_type': 'Fast Food',
        'address': 'Guanzon St/City Proper, Kabankalan City',
        'opening_hours': '9AM - 9PM',
        'image': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80',
        'description': 'Well-known Philippines fast-food chain.',
        'lat': '9.9899', 'lng': '122.8146', # Exact Coordinates
        'menu': [
            {'name': 'Chickenjoy (1pc)', 'price': '₱85'},
            {'name': 'Jolly Spaghetti', 'price': '₱60'},
            {'name': 'Yumburger', 'price': '₱45'},
        ]
    },
    {
        'id': 2, 'name': 'Mang Inasal (CityMall)', 'cuisine_type': 'Local & Cansi',
        'address': 'Level 1, CityMall Kabankalan, Justice Perez Highway',
        'opening_hours': '8AM - 10PM',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80',
        'description': 'Home of the famous Chicken Inasal.',
        'lat': '9.9938', 'lng': '122.8180',
        'menu': [
            {'name': 'Paborito Meal (PM1)', 'price': '₱120'},
            {'name': 'Unli Rice', 'price': '₱35'},
        ]
    },
    {
        'id': 3, 'name': "McDonald's", 'cuisine_type': 'Fast Food',
        'address': 'Guanzon St., Kabankalan City',
        'opening_hours': 'Open 24/7',
        'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500&q=80',
        'description': 'I\'m lovin\' it.',
        'lat': '9.9885', 'lng': '122.8140',
        'menu': [
            {'name': 'Big Mac', 'price': '₱150'},
            {'name': 'Fries (Medium)', 'price': '₱65'},
        ]
    },
    {
        'id': 4, 'name': 'Chowking', 'cuisine_type': 'Fast Food',
        'address': 'City Proper, Kabankalan',
        'opening_hours': 'Open Daily',
        'image': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&q=80',
        'description': 'Chinese-style fast food.',
        'lat': '9.9905', 'lng': '122.8160',
        'menu': [
            {'name': 'Chao Fan w/ Siomai', 'price': '₱95'},
            {'name': 'Beef Wanton Mami', 'price': '₱110'},
        ]
    },
    {
        'id': 5, 'name': 'Taza La Bien', 'cuisine_type': 'Cafe & Snacks',
        'address': 'Los Angeles St, Brgy. 1',
        'opening_hours': '10AM - 10PM',
        'image': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500&q=80',
        'description': 'Coffee, pastries, and pasta.',
        'lat': '9.9910', 'lng': '122.8175',
        'menu': [
            {'name': 'Iced Latte', 'price': '₱120'},
            {'name': 'Carbonara', 'price': '₱150'},
        ]
    },
    {
        'id': 6, 'name': "ALONSO's Cansi & Sizzling House", 'cuisine_type': 'Local & Cansi',
        'address': 'Guanzon St, Brgy. 1',
        'opening_hours': 'Open 24/7',
        'image': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
        'description': 'Famous Cansi and Sizzling Sisig.',
        'lat': '9.9900', 'lng': '122.8165',
        'menu': [
            {'name': 'Cansi (Good for 2)', 'price': '₱180'},
            {'name': 'Sizzling Sisig', 'price': '₱130'},
        ]
    },
    {
        'id': 7, 'name': "Myrna's Restaurant", 'cuisine_type': 'Local & Cansi',
        'address': 'Tan Lorenzo Street, Kabankalan City',
        'opening_hours': '8AM - 8PM',
        'image': 'https://images.unsplash.com/photo-1626776876729-bab4369a5a5a?w=500&q=80',
        'description': 'Filipino home-cooked meals.',
        'lat': '9.9895', 'lng': '122.8150',
        'menu': [
            {'name': 'Pork Adobo w/ Rice', 'price': '₱85'},
            {'name': 'Sinigang na Baboy', 'price': '₱120'},
        ]
    },
    {
        'id': 8, 'name': "3RD Talabahan", 'cuisine_type': 'Local & Cansi',
        'address': 'Lirazan Street, Kabankalan City',
        'opening_hours': '10AM - 10PM',
        'image': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=500&q=80',
        'description': 'Fresh seafood and grilled fish.',
        'lat': '9.9890', 'lng': '122.8170',
        'menu': [
            {'name': 'Grilled Fish', 'price': '₱150'},
            {'name': 'Buttered Shrimp', 'price': '₱200'},
        ]
    },
    {
        'id': 9, 'name': "Mang Inasal (Gaisano)", 'cuisine_type': 'Fast Food',
        'address': 'Gaisano Grand Mall Kabankalan, Brgy. 1',
        'opening_hours': '10AM - 9PM',
        'image': 'https://images.unsplash.com/photo-1598514982205-f36b96d1e8dd?w=500&q=80',
        'description': 'Chicken Inasal near Gaisano Mall.',
        'lat': '9.9875', 'lng': '122.8120',
        'menu': [
            {'name': 'Paborito Meal (PM1)', 'price': '₱120'},
            {'name': 'Pork BBQ (2 sticks)', 'price': '₱75'},
        ]
    }
]


def restaurant_list(request):
    restaurants = RESTAURANTS_DATA.copy()
    query = request.GET.get('q', '')
    cuisine_filter = request.GET.get('cuisine', '')

    if query:
        restaurants = [r for r in restaurants if query.lower() in r['name'].lower() or query.lower() in r['address'].lower()]
    if cuisine_filter:
        restaurants = [r for r in restaurants if r['cuisine_type'] == cuisine_filter]

    return render(request, 'restaurant_list.html', {
        'restaurants': restaurants, 
        'query': query, 
        'current_cuisine': cuisine_filter
    })


def restaurant_detail(request, pk):
    restaurant = next((r for r in RESTAURANTS_DATA if r['id'] == pk), None)
    if restaurant is None:
        return redirect('food_finder:restaurant_list')

    encoded_address = urllib.parse.quote(restaurant['address'])
    restaurant['map_embed'] = f"https://maps.google.com/maps?q={encoded_address}&t=&z=16&ie=UTF8&iwloc=&output=embed"
    restaurant['map_link'] = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})


def restaurant_map(request):
    # Ipapasa natin ang buong listahan para sa sidebar ng mapa
    return render(request, 'map.html', {'restaurants': RESTAURANTS_DATA})


# ==========================================
# IBANG FUNCTIONS
# ==========================================
@login_required
def add_review(request, pk): return redirect('food_finder:restaurant_list')

@login_required
def toggle_favorite(request, pk): return redirect('food_finder:restaurant_list')

@login_required
def my_favorites(request): return render(request, 'my_favorites.html', {'favorites': []})

@login_required
def add_restaurant(request): return redirect('food_finder:restaurant_list')