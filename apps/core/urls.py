from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Existing paths
    path('login/', views.login_view, name='login'), 
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- MGA PATH PARA SA MGA CARDS ---
    path('near-me/', views.near_me_view, name='near_me'),
    path('top-rated/', views.top_rated_view, name='top_rated'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('promos/', views.promos_view, name='promos'),
    
    # --- BAGONG PATH PARA SA RESTAURANT DETAILS ---
    # Ito ang hinahanap ng Django kapag clinick mo ang isang restaurant
    path('restaurant/<int:rest_id>/', views.restaurant_detail_view, name='restaurant_detail'),
]