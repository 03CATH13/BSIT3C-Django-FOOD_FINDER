from django.urls import path
from . import views

app_name = 'food_finder'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('about/', views.about_view, name='about'),
    path('map/', views.restaurant_map, name='restaurant_map'),
    path('register/', views.register_view, name='register'),
    
    # --- PLACE ORDER ---
    path('place-order/<int:pk>/', views.place_order, name='place_order'),
    
    # --- TOGGLE FAVORITE ---
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    
    # --- RESTAURANT DETAIL (DAPAT NAAS UBOS) ---
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
]