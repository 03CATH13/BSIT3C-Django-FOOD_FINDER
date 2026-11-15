import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import logout, authenticate, login
from .models import Restaurant, Review


# ============================================================
# FOOD DATA
# ============================================================
FOOD_DATA = {
    "fastfood": [
        {
            "name": "Jollibee (Guanzon)",
            "mapQuery": "Jollibee+Guanzon+St+Kabankalan",
            "rating": "4.5",
            "price": "₱100–₱200",
            "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, Kabankalan City Proper",
            "menu": [
                {"name": "Chickenjoy", "price": "₱99", "desc": "Crispy fried chicken",
                 "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "McDonald's (Guanzon)",
            "mapQuery": "McDonalds+Guanzon+St+Kabankalan",
            "rating": "4.3",
            "price": "₱80–₱180",
            "img": "https://images.unsplash.com/photo-1550547660-d9450f859349?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, Kabankalan City Proper",
            "menu": [
                {"name": "Big Mac", "price": "₱180", "desc": "Double burger",
                 "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Mang Inasal (Gaisano)",
            "mapQuery": "Gaisano+Grand+Mall+Kabankalan",
            "rating": "4.4",
            "price": "₱120–₱250",
            "img": "https://images.unsplash.com/photo-1513639776629-7b61b0ac49cb?q=80&w=800&auto=format&fit=crop",
            "address": "Gaisano Grand Mall, City Proper",
            "menu": [
                {"name": "1pc Chicken", "price": "₱110", "desc": "Original recipe",
                 "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Chowking (City Mall)",
            "mapQuery": "Chowking+City+Mall+Kabankalan",
            "rating": "4.1",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=800&auto=format&fit=crop",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Chao Fan", "price": "₱95", "desc": "Fried rice",
                 "img": "https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Angel's Burger (Rizal)",
            "mapQuery": "Angels+Burger+Rizal+Kabankalan",
            "rating": "4.2",
            "price": "₱25–₱60",
            "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Burger Steak", "price": "₱35", "desc": "Classic burger",
                 "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Lola Nena's Lomi",
            "mapQuery": "Lomi+House+Tan+Lorenzo+Kabankalan",
            "rating": "4.7",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=800&auto=format&fit=crop",
            "address": "Tan Lorenzo St, City Proper",
            "menu": [
                {"name": "Special Lomi", "price": "₱90", "desc": "Noodle soup",
                 "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=200&auto=format&fit=crop"}
            ],
        },
    ],
    "carinderia": [
        {
            "name": "ALONSO's Cansi",
            "mapQuery": "Alonsos+Cansi+Guanzon+Kabankalan",
            "rating": "4.8",
            "price": "₱150–₱300",
            "img": "https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, Brgy. 1, City Proper",
            "menu": [
                {"name": "Special Cansi", "price": "₱130", "desc": "Sour beef soup",
                 "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Kabankalan Ihaw-Ihaw",
            "mapQuery": "Rizal+Street+Kabankalan+City",
            "rating": "4.9",
            "price": "₱50–₱150",
            "img": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Pork BBQ", "price": "₱100", "desc": "Grilled skewers",
                 "img": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Cansi House",
            "mapQuery": "Cansi+House+Rizal+Kabankalan",
            "rating": "4.7",
            "price": "₱120–₱280",
            "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, Brgy. 5, City Proper",
            "menu": [
                {"name": "Cansi Bulalo", "price": "₱280", "desc": "Rich soup",
                 "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Sharyn's Cansi",
            "mapQuery": "Sharyns+Cansi+National+Highway+Kabankalan",
            "rating": "4.6",
            "price": "₱150–₱260",
            "img": "https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=800&auto=format&fit=crop",
            "address": "National Highway, Brgy. 1, City Proper",
            "menu": [
                {"name": "Special Cansi", "price": "₱260", "desc": "Sour soup",
                 "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Aida's Carinderia",
            "mapQuery": "Kabankalan+City+Public+Market",
            "rating": "4.5",
            "price": "₱50–₱100",
            "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=800&auto=format&fit=crop",
            "address": "Public Market, City Proper",
            "menu": [
                {"name": "Adobo with Rice", "price": "₱70", "desc": "Classic adobo",
                 "img": "https://images.unsplash.com/photo-1626804475297-41609ea0d498?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Tita Beth's Eatery",
            "mapQuery": "Guanzon+Street+Kabankalan+City",
            "rating": "4.6",
            "price": "₱60–₱120",
            "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St., Brgy. 2, City Proper",
            "menu": [
                {"name": "Kare-Kare", "price": "₱120", "desc": "Peanut stew",
                 "img": "https://images.unsplash.com/photo-1626804475297-41609ea0d498?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Myrna's Restaurant",
            "mapQuery": "Myrnas+Restaurant+Kabankalan",
            "rating": "4.4",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1626776876729-bab4369a5a5a?q=80&w=800&auto=format&fit=crop",
            "address": "Tan Lorenzo St, City Proper",
            "menu": [
                {"name": "Pork Adobo", "price": "₱85", "desc": "Home-cooked",
                 "img": "https://images.unsplash.com/photo-1626804475297-41609ea0d498?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "3RD Talabahan",
            "mapQuery": "3RD+Talabahan+Lirazan+Kabankalan",
            "rating": "4.5",
            "price": "₱100–₱250",
            "img": "https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=800&auto=format&fit=crop",
            "address": "Lirazan St, City Proper",
            "menu": [
                {"name": "Baked Talaba", "price": "₱150", "desc": "Fresh oysters",
                 "img": "https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=200&auto=format&fit=crop"}
            ],
        },
    ],
    "cafe": [
        {
            "name": "Gorio's Cafe",
            "mapQuery": "Gorios+Cafe+Kabankalan",
            "rating": "4.9",
            "price": "₱100–₱250",
            "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, Kabankalan City Proper",
            "menu": [
                {"name": "Iced Latte", "price": "₱120", "desc": "Espresso and milk",
                 "img": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Taza La Bien",
            "mapQuery": "Taza+La+Bien+Kabankalan",
            "rating": "4.8",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=800&auto=format&fit=crop",
            "address": "Los Angeles St, Brgy. 1, City Proper",
            "menu": [
                {"name": "Caffe Latte", "price": "₱120", "desc": "Steamed milk",
                 "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Kalamay Artisan Cafe",
            "mapQuery": "Kalamay+Artisan+Lirazan+Kabankalan",
            "rating": "4.6",
            "price": "₱100–₱200",
            "img": "https://images.unsplash.com/photo-1445116572660-236099ec97a0?q=80&w=800&auto=format&fit=crop",
            "address": "Lirazan St, Brgy. 4, City Proper",
            "menu": [
                {"name": "Cappuccino", "price": "₱110", "desc": "Milk foam",
                 "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Kapehan sa Plaza",
            "mapQuery": "Kabankalan+City+Plaza",
            "rating": "4.5",
            "price": "₱30–₱100",
            "img": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?q=80&w=800&auto=format&fit=crop",
            "address": "Plaza Area, Brgy. 1, City Proper",
            "menu": [
                {"name": "Native Coffee", "price": "₱30", "desc": "Brewed coffee",
                 "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "MOICA Pizzeria",
            "mapQuery": "MOICA+Pizzeria+Coloso+Kabankalan",
            "rating": "4.7",
            "price": "₱150–₱400",
            "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=800&auto=format&fit=crop",
            "address": "Coloso St, Brgy. 6, City Proper",
            "menu": [
                {"name": "Pepperoni Pizza", "price": "₱350", "desc": "Classic pizza",
                 "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Amore Mio Pizza",
            "mapQuery": "Amore+Mio+Pizza+Rizal+Kabankalan",
            "rating": "4.6",
            "price": "₱120–₱350",
            "img": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, Brgy. 9, City Proper",
            "menu": [
                {"name": "Margherita", "price": "₱299", "desc": "Italian pizza",
                 "img": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Bo's Coffee (CityMall)",
            "mapQuery": "Bos+Coffee+City+Mall+Kabankalan",
            "rating": "4.4",
            "price": "₱100–₱180",
            "img": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=800&auto=format&fit=crop",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Brewed Coffee", "price": "₱100", "desc": "Local beans",
                 "img": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=200&auto=format&fit=crop"}
            ],
        },
    ],
    "desserts": [
        {
            "name": "Cake Avenue",
            "mapQuery": "Cake+Avenue+Rizal+Kabankalan",
            "rating": "4.7",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Chocolate Cake", "price": "₱120", "desc": "Chocolate slice",
                 "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Melting Pot",
            "mapQuery": "Melting+Pot+Rizal+Kabankalan",
            "rating": "4.4",
            "price": "₱55–₱165",
            "img": "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, Brgy. 7, City Proper",
            "menu": [
                {"name": "Sundae", "price": "₱55", "desc": "Ice cream",
                 "img": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Bibingka Station",
            "mapQuery": "Kabankalan+City+Church",
            "rating": "4.9",
            "price": "₱40–₱100",
            "img": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?q=80&w=800&auto=format&fit=crop",
            "address": "Church Vicinity, City Proper",
            "menu": [
                {"name": "Bibingka", "price": "₱50", "desc": "Rice cake",
                 "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Leche Flan ni Aling Rosa",
            "mapQuery": "Kabankalan+Public+Market",
            "rating": "4.8",
            "price": "₱60–₱120",
            "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?q=80&w=800&auto=format&fit=crop",
            "address": "Public Market, City Proper",
            "menu": [
                {"name": "Leche Flan", "price": "₱70", "desc": "Caramel custard",
                 "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Don Benito's",
            "mapQuery": "Don+Benitos+Guanzon+Kabankalan",
            "rating": "4.5",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, City Proper",
            "menu": [
                {"name": "Halo-Halo", "price": "₱99", "desc": "Shaved ice dessert",
                 "img": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Red Ribbon (CityMall)",
            "mapQuery": "Red+Ribbon+City+Mall+Kabankalan",
            "rating": "4.6",
            "price": "₱100–₱200",
            "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=800&auto=format&fit=crop",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Black Forest", "price": "₱120", "desc": "Cake slice",
                 "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=200&auto=format&fit=crop"}
            ],
        },
    ],
    "milktea": [
        {
            "name": "Chatime (City Mall)",
            "mapQuery": "CityMall+Kabankalan",
            "rating": "4.8",
            "price": "₱70–₱140",
            "img": "https://images.unsplash.com/photo-1525803377221-4f6ccdaa5133?q=80&w=800&auto=format&fit=crop",
            "address": "City Mall, City Proper",
            "menu": [
                {"name": "Pearl Milk Tea", "price": "₱85", "desc": "Classic pearls",
                 "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Macao Imperial Tea",
            "mapQuery": "Gaisano+Grand+Mall+Kabankalan",
            "rating": "4.6",
            "price": "₱90–₱160",
            "img": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?q=80&w=800&auto=format&fit=crop",
            "address": "Gaisano Grand Mall, City Proper",
            "menu": [
                {"name": "Cream Cheese", "price": "₱120", "desc": "Cheesecake series",
                 "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "CoCo Fresh Tea",
            "mapQuery": "CoCo+Fresh+Tea+Araneta+Kabankalan",
            "rating": "4.5",
            "price": "₱90–₱130",
            "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?q=80&w=800&auto=format&fit=crop",
            "address": "Araneta St, City Proper",
            "menu": [
                {"name": "3Q Milk Tea", "price": "₱110", "desc": "Pearl, pudding, jelly",
                 "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "SereniTea",
            "mapQuery": "SereniTea+Kabankalan",
            "rating": "4.4",
            "price": "₱70–₱120",
            "img": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Wintermelon", "price": "₱75", "desc": "Sweet and refreshing",
                 "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Tea Talk",
            "mapQuery": "Tea+Talk+Guanzon+Kabankalan",
            "rating": "4.3",
            "price": "₱60–₱100",
            "img": "https://images.unsplash.com/photo-1525803377221-4f6ccdaa5133?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, City Proper",
            "menu": [
                {"name": "Okinawa", "price": "₱85", "desc": "Brown sugar milk tea",
                 "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?q=80&w=200&auto=format&fit=crop"}
            ],
        },
        {
            "name": "Infinitea",
            "mapQuery": "Infinitea+Kabankalan",
            "rating": "4.5",
            "price": "₱80–₱130",
            "img": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?q=80&w=800&auto=format&fit=crop",
            "address": "City Proper, Kabankalan",
            "menu": [
                {"name": "Hokkaido", "price": "₱95", "desc": "Creamy milk tea",
                 "img": "https://images.unsplash.com/photo-1525803377221-4f6ccdaa5133?q=80&w=200&auto=format&fit=crop"}
            ],
        },
    ],
}


# ============================================================
# TRENDING NAMES
# ============================================================
TRENDING_NAMES = [
    ("fastfood", "Jollibee (Guanzon)"),
    ("fastfood", "Mang Inasal (Gaisano)"),
    ("carinderia", "Kabankalan Ihaw-Ihaw"),
    ("carinderia", "ALONSO's Cansi"),
    ("cafe", "Taza La Bien"),
    ("desserts", "Bibingka Station"),
    ("milktea", "Chatime (City Mall)"),
    ("milktea", "Macao Imperial Tea"),
]


def get_trending_data():
    trending = []
    for category, name in TRENDING_NAMES:
        for item in FOOD_DATA.get(category, []):
            if item["name"] == name:
                trending.append(item)
                break
    return trending


# ============================================================
# HOME VIEW
# ============================================================
def home(request):
    reviews = Review.objects.all().order_by('-created_at')
    context = {
        'food_data': json.dumps(FOOD_DATA),
        'trending_data': json.dumps(get_trending_data()),
        'reviews': reviews,
    }
    return render(request, 'index.html', context)


# ============================================================
# ABOUT
# ============================================================
def about(request):
    context = {
        'title': 'About Kabankalan Eats',
        'description': 'Kabankalan Eats is your dedicated local food guide, exclusively covering the heart of Kabankalan City Proper. We built this platform to help locals and visitors easily discover the best local restaurants, hidden food gems, and trending cafes in the city.',
        'features': [
            {'icon': '🔍', 'title': 'Discover Local Restaurants', 'desc': 'Makapangita ka sang mga kainan sa Kabankalan City Proper. Gikan sa mga local nga pagkaon pareho sang Cansi, fast-food, desserts, cafe and milk tea shops.'},
            {'icon': '📂', 'title': 'Browse by Category', 'desc': 'Pwede ka magpili sang kategorya sang pagkaon nga gusto mo — halin sa Local Favorites, Fast Food, Cafe, Cansi tubtob sa Milk Tea shop.'},
            {'icon': '🍽️', 'title': 'View Full Menu & Prices', 'desc': 'Makita mo dayon ang menu, presyo, kag detalye sang kada pagkaon, para kabalo ka na kung ano orderon mo bag-o ka pa magkadto.'},
            {'icon': '⭐', 'title': 'Ratings & Reviews', 'desc': 'Makabasa ka sang reviews sang iban, kag makahatag ka man sang imo kaugalingon nga rating kag review.'},
            {'icon': '🔥', 'title': 'Trending Spots', 'desc': 'Makita mo kung ano ang pinaka-trending kag ginadagsa nga kalan-an subong sa Kabankalan.'},
            {'icon': '📍', 'title': 'Map & Location', 'desc': 'May kompleto nga address kag map link ang kada restaurant, para dali mo gid sila makit-an kag indi ka na maglibog kung din ka magkadto.'},
        ]
    }
    return render(request, 'about.html', context)


# ============================================================
# LOGOUT
# ============================================================
def logout_user(request):
    logout(request)
    return redirect('food_finder:home')


# ============================================================
# LOGIN
# ============================================================
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('food_finder:home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    return render(request, 'login.html')


# ============================================================
# SUBMIT REVIEW (AJAX)
# ============================================================
@require_POST
def submit_review(request):
    name = request.POST.get('name', '').strip()
    rating = request.POST.get('rating', '5')
    text = request.POST.get('text', '').strip()

    if not name or not text:
        return JsonResponse({'ok': False, 'error': 'Missing fields'}, status=400)

    review = Review.objects.create(name=name, rating=int(rating), text=text)
    return JsonResponse({
        'ok': True,
        'name': review.name,
        'rating': review.rating,
        'stars': review.stars_display,
        'text': review.text,
        'date': review.created_at.strftime('%B %d, %Y'),
    })