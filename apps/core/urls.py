from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('near-me/', views.near_me_view, name='near_me'),
    path('top-rated/', views.top_rated_view, name='top_rated'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('promos/', views.promos_view, name='promos'),
    path('restaurant/<int:rest_id>/', views.restaurant_detail_view, name='restaurant_detail'),
    path('place-order/<int:rest_id>/', views.place_order, name='place_order'),
]