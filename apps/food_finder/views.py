from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import logout, authenticate, login
from .models import Restaurant, Review

def home(request):
    # Kinukuha natin ang data mula sa database at ginagawang JSON format
    food_data = {}

    # Loop sa bawat category
    for cat_key, _ in Restaurant.CATEGORY_CHOICES:
        restaurants = Restaurant.objects.filter(category=cat_key)
        food_data[cat_key] = []
        for r in restaurants:
            menu_list = []
            # Kunin ang mga menu ng restaurant na ito
            for m in r.menu_items.all():
                menu_list.append({
                    'name': m.name,
                    'price': m.price,
                    'desc': m.desc,
                    'img': m.img,
                })

            # Isama ang restaurant sa listahan
            food_data[cat_key].append({
                'name': r.name,
                'mapQuery': r.map_query,
                'rating': r.rating,
                'price': r.price_range,
                'img': r.img,
                'address': r.address,
                'is_trending': r.is_trending,
                'menu': menu_list,
            })

    reviews = Review.objects.all()

    context = {
        'restaurant_data': food_data,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)

# ===== DIRI ANG ABOUT MO, CHAKTO NA ====
def about(request):
    context = {
        'title': 'About Kabankalan Eats',
        'description': 'Kabankalan Eats is your dedicated local food guide, exclusively covering the heart of Kabankalan City Proper. We built this platform to help locals and visitors easily discover the best local restaurants, hidden food gems, and trending cafes in the city.',
        'features': [
            {
                'icon': '🔍',
                'title': 'Discover Local Restaurants',
                'desc': 'Makapangita ka sang mga kainan sa Kabankalan City Proper. Gikan sa mga local nga pagkaon pareho sang Cansi, fast-food ,desserts , cafe and milk tea shops.'
            },
            {
                'icon': '📂',
                'title': 'Browse by Category',
                'desc': 'Pwede ka magpili sang kategorya sang pagkaon nga gusto mo — halin sa Local Favorites, Fast Food, Cafe, Cansi tubtob sa Milk Tea shop.'
            },
            {
                'icon': '🍽️',
                'title': 'View Full Menu & Prices',
                'desc': 'Makita mo dayon ang menu, presyo, kag detalye sang kada pagkaon, para kabalo ka na kung ano orderon mo bag-o ka pa magkadto..'
            },
            {
                'icon': '⭐',
                'title': 'Ratings & Reviews',
                'desc': 'Makabasa ka sang reviews sang iban, kag makahatag ka man sang imo kaugalingon nga rating kag review.'
            },
            {
                'icon': '🔥',
                'title': 'Trending Spots',
                'desc': 'Makita mo kung ano ang pinaka-trending kag ginadagsa nga kalan-an subong sa Kabankalan.'
            },
            {
                'icon': '📍',
                'title': 'Map & Location',
                'desc': 'May kompleto nga address kag map link ang kada restaurant, para dali mo gid sila makit-an kag indi ka na maglibog kung din ka magkadto.'
            },
        ]
    }
    return render(request, 'about.html', context)
# ===== TAPOS ANG ABOUT =====

def logout_user(request):
    logout(request)
    return redirect('food_finder:home')

# ===== BAG-O NI, ANG LOGIN MO ====
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('food_finder:home')
        else:
            return render(request, 'login.html', {'error': 'Sala ang username ukon password.'})
    return render(request, 'login.html')
# ===== TAPOS ANG LOGIN =====

@require_POST
def submit_review(request):
    name = request.POST.get('name', '').strip()
    rating = request.POST.get('rating', '5')
    text = request.POST.get('text', '').strip()

    if not name or not text:
        return JsonResponse({'ok': False, 'error': 'Missing fields'}, status=400)

    review = Review.objects.create(name=name, rating=int(rating), text=text)
    return JsonResponse({
        'ok': True,
        'name': review.name,
        'rating': review.rating,
        'stars': review.stars_display,
        'text': review.text,
        'date': review.created_at.strftime('%B %d, %Y'),
    })