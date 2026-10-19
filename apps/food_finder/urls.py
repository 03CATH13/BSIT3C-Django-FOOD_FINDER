from django.urls import path
from . import views

app_name = 'food_finder'

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
]