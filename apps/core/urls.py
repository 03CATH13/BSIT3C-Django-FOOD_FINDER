from django.urls import path
from . import views
from apps.food_finder.views import register_view  # <--- Import ang register_view

app_name = 'core'

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Register Page (Gikan sa food_finder app)
    path('register/', register_view, name='register'),

    # Finder Pages
    path('near-me/', views.near_me_view, name='near_me'),
    path('top-rated/', views.top_rated_view, name='top_rated'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('promos/', views.promos_view, name='promos'),

    # Detail & Ordering Pages
    path('restaurant/<int:rest_id>/', views.restaurant_detail_view, name='restaurant_detail'),
    path('place-order/<int:rest_id>/', views.place_order, name='place_order'),
]