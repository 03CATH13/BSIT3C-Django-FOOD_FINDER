from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Restaurant, MenuItem, Review, Favorite


def restaurant_list(request):
    """Show all restaurants with optional search & filter."""
    query = request.GET.get('q', '')
    cuisine = request.GET.get('cuisine', '')

    restaurants = Restaurant.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(description__icontains=query)
        )
    if cuisine:
        restaurants = restaurants.filter(cuisine_type=cuisine)

    # Annotate average rating
    restaurants = restaurants.annotate(avg_rating=Avg('reviews__rating'))

    context = {
        'restaurants': restaurants,
        'query': query,
        'cuisine': cuisine,
        'cuisine_choices': Restaurant.CUISINE_CHOICES,
    }
    # BINAGO: Tinanggal ang 'finder/'
    return render(request, 'restaurant_list.html', context)


def restaurant_detail(request, pk):
    """Show details of one restaurant including menu and reviews."""
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu_items = restaurant.menu_items.filter(is_available=True)
    reviews = restaurant.reviews.all()
    avg_rating = restaurant.average_rating()

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=request.user, restaurant=restaurant
        ).exists()

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_favorited': is_favorited,
    }
    # BINAGO: Tinanggal ang 'finder/'
    return render(request, 'restaurant_detail.html', context)


@login_required
def add_review(request, pk):
    """Submit a review for a restaurant."""
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        if Review.objects.filter(user=request.user, restaurant=restaurant).exists():
            messages.warning(request, "You already reviewed this restaurant.")
        else:
            Review.objects.create(
                user=request.user,
                restaurant=restaurant,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Review added successfully!")

    return redirect('finder:restaurant_detail', pk=pk)


@login_required
def toggle_favorite(request, pk):
    """Add or remove a restaurant from favorites."""
    restaurant = get_object_or_404(Restaurant, pk=pk)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user, restaurant=restaurant
    )
    if not created:
        favorite.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Added to favorites!")
    return redirect('finder:restaurant_detail', pk=pk)


@login_required
def my_favorites(request):
    """Show all restaurants the user has favorited."""
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    # BINAGO: Tinanggal ang 'finder/'
    return render(request, 'my_favorites.html', {'favorites': favorites})