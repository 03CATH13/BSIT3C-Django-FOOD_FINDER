from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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