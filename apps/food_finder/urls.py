from django.urls import path
from . import views

app_name = 'food_finder'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/review/', views.submit_review, name='submit_review'),
]