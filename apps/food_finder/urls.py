from django.urls import path
from . import views

app_name = 'food_finder'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.restaurant_list, name='search_results'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('about/', views.about_view, name='about'),
    path('map/', views.restaurant_map, name='restaurant_map'),
    path('register/', views.register_view, name='register'),
    path('place-order/<int:pk>/', views.place_order, name='place_order'),
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('owner/delivered/<int:order_id>/', views.mark_delivered, name='mark_delivered'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
]