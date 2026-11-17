from django.urls import path
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

app_name = 'food_finder'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),        # BAGONG DAGDAG
    path('help/', views.help_page, name='help'),            # BAGONG DAGDAG
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('submit-review/', views.submit_review, name='submit_review'),

    # FIX PARA MADULA ANG: Not Found: /favicon.ico 404
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]