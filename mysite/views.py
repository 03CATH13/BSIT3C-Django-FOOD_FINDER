from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

# --- MGA BAGONG VIEWS PARA SA MGA CARDS (Placeholder) ---
def near_me_view(request):
    return render(request, 'placeholder.html', {'title': 'Near Me'})

def top_rated_view(request):
    return render(request, 'placeholder.html', {'title': 'Top Rated'})

def my_orders_view(request):
    return render(request, 'placeholder.html', {'title': 'My Orders'})

def promos_view(request):
    return render(request, 'placeholder.html', {'title': 'Promos'})