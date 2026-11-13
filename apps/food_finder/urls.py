from django.urls import path
from . import views

app_name = 'food_finder'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('submit-review/', views.submit_review, name='submit_review'),
]