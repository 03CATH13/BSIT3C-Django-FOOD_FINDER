from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from decimal import Decimal, InvalidOperation

# --- DITO ILALAGAY ANG DATA MO ---
RESTAURANT_LIST_DATA = [
    {
        'id': 1, 'name': 'Jollibee', 'cuisine_type': 'Fast Food',
        'address': 'Guanzon St/City Proper, Kabankalan City', 'opening_hours': '9AM - 9PM',
        'image': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80',
        'description': 'Well-known Philippines fast-food chain.', 'lat': '9.99028', 'lng': '122.81472',
        'menu': [{'name': 'Chickenjoy (1pc)', 'price': '₱85'}, {'name': 'Jolly Spaghetti', 'price': '₱60'}, {'name': 'Yumburger', 'price': '₱45'}, {'name': 'Chicken with Rice', 'price': '₱99'}, {'name': 'Chicken Bucket (6pcs)', 'price': '₱499'}, {'name': 'Cheesy Yumburger', 'price': '₱69'}, {'name': 'Jolly Hotdog', 'price': '₱65'}, {'name': 'Burger Steak', 'price': '₱79'}, {'name': 'Palabok Fiesta', 'price': '₱99'}, {'name': 'French Fries', 'price': '₱60'}]
    },
    {
        'id': 2, 'name': 'Mang Inasal (CityMall)', 'cuisine_type': 'Fast Food',
        'address': 'Level 1, CityMall Kabankalan, Justice Perez Highway', 'opening_hours': '8AM - 10PM',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80',
        'description': 'Home of the famous Chicken Inasal.', 'lat': '9.99388', 'lng': '122.81798',
        'menu': [{'name': 'Paborito Meal (PM1)', 'price': '₱120'}, {'name': 'Unli Rice', 'price': '₱35'}, {'name': 'Paa Large Uli Rice', 'price': '₱185'}, {'name': 'Spicy Paa Large', 'price': '₱165'}, {'name': 'Pork Sisig', 'price': '₱165'}, {'name': 'Bangus Sisig', 'price': '₱155'}, {'name': 'Palabok', 'price': '₱85'}, {'name': 'Halo-Halo', 'price': '₱75'}]
    },
    {
        'id': 3, 'name': "McDonald's", 'cuisine_type': 'Fast Food',
        'address': 'Guanzon St., Kabankalan City', 'opening_hours': 'Open 24/7',
        'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500&q=80',
        'description': "I'm lovin' it.", 'lat': '9.98998', 'lng': '122.81442',
        'menu': [{'name': 'Big Mac', 'price': '₱150'}, {'name': 'Fries (Medium)', 'price': '₱65'}, {'name': 'Chicken Mcdo large (1pc)', 'price': '₱125'}, {'name': 'Mc Spaghetti', 'price': '₱75'}, {'name': 'Cheese Burger', 'price': '₱69'}, {'name': 'Mc Chicken Sandwich', 'price': '₱95'}, {'name': 'Fries Large', 'price': '₱75'}, {'name': 'Mc Float', 'price': '₱45'}, {'name': 'Sundae', 'price': '₱35'}]
    },
    {
        'id': 4, 'name': 'Chowking', 'cuisine_type': 'Fast Food',
        'address': 'City Proper, Kabankalan', 'opening_hours': 'Open Daily',
        'image': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&q=80',
        'description': 'Chinese-style fast food.', 'lat': '9.99058', 'lng': '122.81592',
        'menu': [{'name': 'Chao Fan w/ Siomai', 'price': '₱95'}, {'name': 'Beef Wanton Mami', 'price': '₱110'}, {'name': 'Chao Fan + Chicken', 'price': '₱145'}, {'name': 'Sweet & Sour Pork', 'price': '₱135'}, {'name': 'Siomai (4pcs)', 'price': '₱49'}, {'name': 'Halo-Halo', 'price': '₱89'}, {'name': 'BuChi (3pcs)', 'price': '₱55'}]
    },
    {
        'id': 5, 'name': 'Taza La Bien', 'cuisine_type': 'Cafe & Snacks',
        'address': 'Los Angeles St, Brgy. 1', 'opening_hours': '10AM - 10PM',
        'image': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500&q=80',
        'description': 'Coffee, pastries, and pasta.', 'lat': '9.99108', 'lng': '122.81758',
        'menu': [{'name': 'Iced Latte', 'price': '₱120'}, {'name': 'Carbonara', 'price': '₱150'}, {'name': 'Wintermelon Milktea', 'price': '₱75'}, {'name': 'Okinawa Milktea', 'price': '₱80'}, {'name': 'Taro Milktea', 'price': '₱80'}, {'name': 'Americano Coffe', 'price': '₱90'}, {'name': 'Spanish Latte', 'price': '₱110'}, {'name': 'Chicken Wings (6pcs)', 'price': '₱165'}, {'name': 'Fries Overload', 'price': '₱95'}, {'name': 'Nachos', 'price': '₱85'}]
    },
    {
        'id': 6, 'name': "ALONSO's Cansi & Sizzling House", 'cuisine_type': 'Local & Cansi',
        'address': 'Guanzon St, Brgy. 1', 'opening_hours': 'Open 24/7',
        'image': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
        'description': 'Famous Cansi and Sizzling Sisig.', 'lat': '9.99008', 'lng': '122.81652',
        'menu': [{'name': 'Cansi (Good for 2)', 'price': '₱180'}, {'name': 'Sizzling Sisig', 'price': '₱130'}, {'name': 'Special Cansi', 'price': '₱280'}, {'name': 'Bone Marrow Cansi', 'price': '₱380'}, {'name': 'Sizzling Cansi', 'price': '₱250'}, {'name': 'Sizzling Pork Sisig', 'price': '₱185'}, {'name': 'Sizzling Bulalo', 'price': '₱295'}, {'name': 'Cansi Batchoy', 'price': '₱120'}, {'name': 'Grilled Liempo', 'price': '₱195'}]
    },
    {
        'id': 7, 'name': "Myrna's Restaurant", 'cuisine_type': 'Local & Cansi',
        'address': 'Tan Lorenzo Street, Kabankalan City', 'opening_hours': '8AM - 8PM',
        'image': 'https://images.unsplash.com/photo-1626776876729-bab4369a5a5a?w=500&q=80',
        'description': 'Filipino home-cooked meals.', 'lat': '9.98958', 'lng': '122.81508',
        'menu': [{'name': 'Pork Adobo w/ Rice', 'price': '₱85'}, {'name': 'Sinigang na Baboy', 'price': '₱120'}, {'name': 'Chicken Inasal Pecho', 'price': '₱145'}, {'name': 'Pork BBQ (3sticks)', 'price': '₱135'}, {'name': 'Kansi', 'price': '₱240'}, {'name': 'Linaga', 'price': '₱220'}, {'name': 'Batchoy', 'price': '₱95'}, {'name': 'Pancit Bam-i', 'price': '₱125'}, {'name': 'Garlic Rice', 'price': '₱30'}]
    },
    {
        'id': 8, 'name': '3RD Talabahan', 'cuisine_type': 'Local & Cansi',
        'address': 'Lirazan Street, Kabankalan City', 'opening_hours': '10AM - 10PM',
        'image': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=500&q=80',
        'description': 'Fresh seafood and grilled fish.', 'lat': '9.98898', 'lng': '122.81698',
        'menu': [{'name': 'Grilled Fish', 'price': '₱150'}, {'name': 'Buttered Shrimp', 'price': '₱200'}, {'name': 'Baked Talaba', 'price': '₱150'}, {'name': 'Butter Garlic Talaba', 'price': '₱200'}, {'name': 'Sizzling Squid', 'price': '₱195'}, {'name': 'Grilled Fish', 'price': '₱180'}, {'name': 'Sinigang Hipon', 'price': '₱220'}, {'name': 'Beer Bucket', 'price': '₱350'}]
    },
    {
        'id': 9, 'name': 'Mang Inasal (Gaisano)', 'cuisine_type': 'Fast Food',
        'address': 'Gaisano Grand Mall Kabankalan, Brgy. 1', 'opening_hours': '10AM - 9PM',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80',
        'description': 'Chicken Inasal near Gaisano Mall.', 'lat': '9.98758', 'lng': '122.81208',
        'menu': [{'name': 'Paborito Meal (PM1)', 'price': '₱120'}, {'name': 'Pork BBQ (2 pcs)', 'price': '₱145'}, {'name': 'Halo-Halo Small', 'price': '₱75'}, {'name': 'Halo-Halo Large', 'price': '₱95'}, {'name': 'Palabok', 'price': '₱90'}, {'name': 'Paa Large Unli Rice', 'price': '₱175'}, {'name': 'Pecho Large Unli Rice', 'price': '₱185'}, {'name': 'Paa Small', 'price': '₱135'}, {'name': 'Chicken Inasal with Sinigang', 'price': '₱195'}, {'name': 'Extra Unli Rice', 'price': '₱25'}, {'name': 'Coke Mismo', 'price': '₱25'}]
    },
    {
        'id': 10, 'name': 'Kalamay Artisan Patisserie & Cafe', 'cuisine_type': 'Cafe & Snacks',
        'address': '42 Lirazan St. Brgy. 4 Kabankalan City', 'opening_hours': '8AM - 8PM',
        'image': 'https://th.bing.com/th/id/OIP.Ly_7Z5aIAM0qNIUagX_JLAHaE8?r=0&pid=CanonicalCanvas',
        'description': 'Classic British menu, European breads and pasties.', 'lat': '9.98708', 'lng': '122.81358',
        'menu': [{'name': 'British Paties', 'price': '₱120'}, {'name': 'Coffe Latte', 'price': '₱95'}, {'name': 'Fresh Salad', 'price': '₱120'}, {'name': 'Chicken Pasties', 'price': '₱130'}, {'name': 'Cappuccino', 'price': '₱110'}, {'name': 'Croissant Plain', 'price': '₱85'}, {'name': 'Pain au Chocolat', 'price': '₱95'}, {'name': 'Ensaymada Special', 'price': '₱65'}, {'name': 'Ube Cheese Pandesal (6pcs)', 'price': '₱90'}, {'name': 'Caramel latte', 'price': '₱125'}, {'name': 'Chicken Pasties', 'price': '₱130'}, {'name': 'Chocolate Cake Slice', 'price': '₱125'}]
    },
    {
        'id': 11, 'name': 'Amore Mio Pizza & Inasal', 'cuisine_type': 'Cafe & Snacks',
        'address': 'SNC Building, Rizal St. Brgy. 9, Kabankalan City', 'opening_hours': '10AM - 9PM',
        'image': 'https://th.bing.com/th/id/OIP.xjw55CL1DD1fxRTe8L42QAHaHa?r=0&pid=CanonicalCanvas',
        'description': 'Authentic wood-fired Italian Pizza by Italian Pizzaiolo.', 'lat': '9.98608', 'lng': '122.81408',
        'menu': [{'name': 'Margherita Pizza', 'price': '₱299'}, {'name': 'Chicken Inasal Paa', 'price': '₱135'}, {'name': 'Pepperino Pugon Pizza', 'price': '₱320'}, {'name': 'Hawaiian Pizza', 'price': '₱320'}, {'name': 'Garlic Bread', 'price': '₱75'}, {'name': 'Four Cheese Pizza', 'price': '₱350'}, {'name': 'Pork BBQ', 'price': '₱45'}, {'name': 'Lasagna', 'price': '₱165'}, {'name': 'Milktea Taro', 'price': '₱75'}]
    },
    {
        'id': 12, 'name': 'Chicken Ati-Atihan', 'cuisine_type': 'Local & Cansi',
        'address': 'Guanzon St. Brgy. 2, Kabankalan City', 'opening_hours': '9AM - 9PM',
        'image': 'https://tse2.mm.bing.net/th/id/OIP.DjvJRW80K48q_WU7degRkwAAAA?r=0&rs=1&pid=ImgDetMain&o=7&rm=3',
        'description': 'Filipino Grill and Chicken dishes.', 'lat': '9.98858', 'lng': '122.81008',
        'menu': [{'name': 'Chicken Inasal Paa', 'price': '₱120'}, {'name': 'Pork BBQ (2 sticks)', 'price': '₱80'}, {'name': 'Chicken Inasal Pecho', 'price': '₱135'}, {'name': 'Pork Liempo', 'price': '₱180'}, {'name': 'Bangus Sisig', 'price': '₱160'}, {'name': 'Garlic Rice', 'price': '₱30'}, {'name': 'Chicken Pecho', 'price': '₱135'}, {'name': 'Chicken Paa', 'price': '₱125'}, {'name': 'Isol', 'price': '₱25'}, {'name': 'Liver', 'price': '₱20'}, {'name': 'Unli Rice', 'price': '₱30'}, {'name': 'Chicken Oil Rice', 'price': '₱35'}, {'name': 'Sizzling Chicken Sisig', 'price': '₱145'}]
    },
    {
        'id': 13, 'name': 'Melting Pot Kabankalan', 'cuisine_type': 'Fast Food',
        'address': 'Rizal St. Brgy. 7, Kabankalan City', 'opening_hours': '9AM - 9PM',
        'image': 'https://th.bing.com/th/id/OLC.i2vkFy008YAnpA480x360?&rs=1&pid=ImgDetMain&o=7&rm=3',
        'description': 'Chicken Inasal near Gaisano Mall.', 'lat': '9.98558', 'lng': '122.81508',
        'menu': [{'name': 'Double Chinese Burger', 'price': '₱165'}, {'name': 'Fries w/ Cheese', 'price': '₱75'}, {'name': 'Spaghetti', 'price': '₱75'}, {'name': 'Sundae Chocolate', 'price': '₱55'}, {'name': 'Chicken Fillet', 'price': '₱99'}, {'name': 'Palabok', 'price': '₱85'}]
    },
    {
        'id': 14, 'name': "Bro's Diner Restaurant", 'cuisine_type': 'Fast Food',
        'address': 'South Gate Inn, Guanzon St. Brgy. 1, Kabankalan City', 'opening_hours': '8AM - 10PM',
        'image': 'https://mms.img.susercontent.com/vn-11134513-7r98o-lsvai0zxaahlc2@resize_ss640x400!@crop_w640_h400_cT',
        'description': 'Diner style meals and quick bites.', 'lat': '9.98958', 'lng': '122.81158',
        'menu': [{'name': 'Tapsilog', 'price': '₱120'}, {'name': 'Burger Steak (2pcs)', 'price': '₱115'}, {'name': 'Longsilog', 'price': '₱110'}, {'name': 'Lomi', 'price': '₱90'}, {'name': 'Lomi Overload', 'price': '₱130'}, {'name': 'Lomi Special', 'price': '₱95'}, {'name': 'Chicksilog', 'price': '₱115'}, {'name': 'Baconsilog', 'price': '₱110'}, {'name': 'Burger w/ Fries', 'price': '₱110'}, {'name': 'Sisig Rice', 'price': '₱115'}]
    },
    {
        'id': 15, 'name': 'Mr. Chow Chinese restaurant', 'cuisine_type': 'Fast food',
        'address': 'ARDC bldg. Guanzon St. Kabankalan City', 'opening_hours': '10AM-9PM',
        'image': 'https://th.bing.com/th/id/OIP.QrvKJSuy6PZSBcmdkAAoRgHaF7?r=0&o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3',
        'description': 'Chinese dishes, Dim sum, Beef specialties.', 'lat': '9.98808', 'lng': '122.81058',
        'menu': [{'name': 'Siomai (4pcs)', 'price': '₱85'}, {'name': 'Siomai (10 pcs)', 'price': '₱120'}, {'name': 'Beef Broccoli', 'price': '₱180'}, {'name': 'Beef Mami', 'price': '₱110'}, {'name': 'Pork Soimai (8pcs)', 'price': '₱150'}, {'name': 'Yang Chow Fried Rice', 'price': '₱140'}, {'name': 'Buchi', 'price': '₱80'}, {'name': 'Beef with Broccoli', 'price': '₱220'}, {'name': 'Siopao Bola-bola', 'price': '₱55'}, {'name': 'Chicken Mami', 'price': '₱95'}, {'name': 'Pancit Canton', 'price': '₱135'}, {'name': 'Sweet & Sour Fish', 'price': '₱195'}, {'name': 'Chopsuey', 'price': '₱145'}, {'name': 'Fried Rice', 'price': '₱90'}]
    },
    {
        'id': 16, 'name': 'MOICA Pizzeria & Bar', 'cuisine_type': 'Cafe & Snacks',
        'address': 'Coloso St. Brgy. 6, Kabankalan City', 'opening_hours': '',
        'image': 'https://tse4.mm.bing.net/th/id/OIP.z7NZBl0obIFnbMdlHsRLBQHaE7?r=0&rs=1&pid=ImgDetMain&o=7&rm=3',
        'description': 'Italian pasta, wood-fired pizza and lasagna.', 'lat': '9.98758', 'lng': '122.81208',
        'menu': [{'name': 'Pepperoni Pizza', 'price': '₱350'}, {'name': 'Pasta Carbonara', 'price': '₱185'}, {'name': 'Four Cheese Pizza', 'price': '₱380'}, {'name': 'Lasagna', 'price': '₱195'}, {'name': 'Spaghetti Bolognese', 'price': '₱165'}, {'name': 'Iced Tea', 'price': '₱60'}, {'name': 'Moica Special Pizza', 'price': '₱420'}, {'name': 'Margherita Pizza', 'price': '₱320'}, {'name': 'Pepperoni Pizza', 'price': '₱350'}, {'name': 'Nachos Overload', 'price': '₱165'}, {'name': 'Beer Below Zero', 'price': 'Price unavailable'}, {'name': 'Iced Coffee', 'price': '₱95'}]
    },
    {
        'id': 17, 'name': 'Cansi House Kabankalan', 'cuisine_type': 'Local & Cansi',
        'address': 'Rizal St. Brgy. 5, Kabankalan City', 'opening_hours': 'Open 24 Hours',
        'image': 'https://tse1.mm.bing.net/th/id/OIP.n2B-8wnf-NuX75YfyMHHOAHaE7?r=1&pid=ImgDetMain&o=7&rm=3',
        'description': 'Original Kabankalan Cansi - sour beef shank soup.', 'lat': '9.98658', 'lng': '122.81308',
        'menu': [{'name': 'Cansi Bulalo', 'price': '₱280'}, {'name': 'Sizzling Cansi', 'price': '₱250'}, {'name': 'Cansi Batchoy', 'price': '₱120'}, {'name': 'Bone Marrow Cansi', 'price': '₱350'}, {'name': 'Special Cansi', 'price': '₱280'}, {'name': 'Bulalo Cansi', 'price': '₱320'}, {'name': 'Cansi Baka', 'price': '₱260'}, {'name': 'Plain Rice', 'price': 'Price unavailable'}]
    },
    {
        'id': 18, 'name': "Sharyn's Cansi", 'cuisine_type': 'Local & Cansi',
        'address': 'National Highway, Brgy. 1, Kabankalan City', 'opening_hours': '7AM-10PM',
        'image': 'https://tse4.mm.bing.net/th/id/OIP.zxuoQgP87JhIM0Bh1YDwngHaJQ?r=0&w=1080&h=1350&rs=1&pid=ImgDetMain&o=7&rm=3',
        'description': 'Famous Cansi and Native Chicken dishes.', 'lat': '9.99008', 'lng': '122.81608',
        'menu': [{'name': 'Special Cansi', 'price': '₱260'}, {'name': 'Native Chicken Tinola', 'price': '₱200'}, {'name': 'KBL (Kadyos Baboy Langka)', 'price': '₱150'}, {'name': 'Linaga Baka', 'price': '₱240'}, {'name': 'Native Tinola Manok', 'price': '₱200'}, {'name': 'Grilled Fish', 'price': '₱160'}, {'name': 'Bam-i Guisado', 'price': '₱125'}]
    },
    {
        'id': 19, 'name': 'RS - Riverside Snack Bar', 'cuisine_type': 'Fast food',
        'address': 'Riverside St. Brgy. 5, Kabankalan City', 'opening_hours': '9AM-7PM',
        'image': 'https://tse2.mm.bing.net/th/id/OIP.z1B9BD5AUVGgkvUVYAD5vgHaE8?r=0&rs=1&pid=ImgDetMain&o=7&rm=3',
        'description': 'Tambayan - fries, burgers and shakes near Riverside.', 'lat': '9.98628', 'lng': '122.81288',
        'menu': [{'name': 'RS Special Burger', 'price': '₱85'}, {'name': 'Cheese Burger', 'price': '₱65'}, {'name': 'Double Cheese Burger', 'price': '₱95'}, {'name': 'French Fries - Small', 'price': '₱40'}, {'name': 'French Fries - Large', 'price': '₱70'}, {'name': 'Cheesy Fries', 'price': '₱85'}, {'name': 'Burger with Fries', 'price': '₱110'}, {'name': 'Chocolate Shake', 'price': '₱60'}, {'name': 'Mango Shake', 'price': '₱65'}, {'name': 'Strawberry Shake', 'price': '₱65'}, {'name': 'Ube Shake', 'price': '₱65'}, {'name': 'Hotdog Sandwich', 'price': '₱45'}]
    },
]

# --- SAMPLE DATA PARA SA TOP RATED ---
TOP_RATED_DATA = [
    {'name': 'Jollibee', 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80', 'reviews': 120},
    {'name': 'Mang Inasal (CityMall)', 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80', 'reviews': 95},
    {'name': 'Kalamay Artisan Patisserie & Cafe', 'rating': 4.7, 'image': 'https://th.bing.com/th/id/OIP.Ly_7Z5aIAM0qNIUagX_JLAHaE8?r=0&pid=CanonicalCanvas', 'reviews': 85},
    {'name': 'Amore Mio Pizza & Inasal', 'rating': 4.6, 'image': 'https://th.bing.com/th/id/OIP.xjw55CL1DD1fxRTe8L42QAHaHa?r=0&pid=CanonicalCanvas', 'reviews': 75},
]

# --- SAMPLE DATA PARA SA PROMOS ---
PROMOS_DATA = [
    {'title': '50% Off First Order', 'code': 'WELCOME50', 'description': 'Valid for new users only. Max discount of ₱100.', 'color': '#eb78bf'},
    {'title': 'Free Delivery', 'code': 'FREEDEL', 'description': 'On orders above ₱500. Valid on weekends.', 'color': '#06b6d4'},
    {'title': 'Buy 1 Take 1', 'code': 'B1T1', 'description': 'On selected Chickenjoy meals. Valid until Oct 31.', 'color': '#f59e0b'},
    {'title': '₱50 Off', 'code': 'SAVE50', 'description': 'Minimum order of ₱300. Valid for all users.', 'color': '#10b981'},
]

def home(request):
    total_orders = 0
    if request.user.is_authenticated:
        total_orders = Order.objects.filter(user=request.user).count()

    context = {
        'total_orders': total_orders,
    }
    return render(request, 'admin/index.html', context) 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/home/')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auth/login.html') 

def logout_view(request):
    logout(request)
    return redirect('core:login')

def near_me_view(request):
    context = {
        'restaurants': RESTAURANT_LIST_DATA
    }
    return render(request, 'admin/near_me.html', context)

@login_required
def restaurant_list_view(request):
    context = {
        'restaurants': RESTAURANT_LIST_DATA,
        'query': request.GET.get('q', ''),
        'current_cuisine': request.GET.get('cuisine', ''),
    }
    return render(request, 'restaurant_list.html', context)

def top_rated_view(request):
    context = {'top_rated': TOP_RATED_DATA}
    return render(request, 'admin/top_rated.html', context)

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    if not orders.exists():
        sample_order = {
            'id': 'SAMPLE-001',
            'restaurant_name': 'Jollibee',
            'items': 'Chickenjoy (1pc), Jolly Spaghetti',
            'total_price': 145.00,
            'status': 'Delivered',
            'created_at': 'Oct 28, 2026 • 12:30 PM'
        }
        context = {'orders': orders, 'sample_order': sample_order}
    else:
        context = {'orders': orders}
    return render(request, 'admin/my_orders.html', context)

def promos_view(request):
    context = {'promos': PROMOS_DATA}
    return render(request, 'admin/promos.html', context)

def restaurant_detail_view(request, rest_id):
    selected_restaurant = None
    for rest in RESTAURANT_LIST_DATA:
        if str(rest['id']) == str(rest_id):
            selected_restaurant = rest
            break
    if not selected_restaurant:
        return redirect('core:near_me')
    context = {'restaurant': selected_restaurant}
    return render(request, 'admin/restaurant_detail.html', context)

@login_required
def place_order(request, rest_id):
    if request.method == 'POST':
        items = request.POST.get('items', '').strip()
        total_price = request.POST.get('total_price', '').strip()
        promo_code = request.POST.get('promo_code', '').strip().upper()
        
        if not total_price:
            total_price = '0.00'
        
        try:
            total_price_decimal = Decimal(total_price)
        except (InvalidOperation, TypeError, ValueError):
            total_price_decimal = Decimal('0.00')
        
        # --- PROMO CODE LOGIC ---
        discount = Decimal('0.00')
        if promo_code == 'WELCOME50':
            discount = total_price_decimal * Decimal('0.50')
        elif promo_code == 'FREEDEL':
            discount = Decimal('50.00')
        elif promo_code == 'B1T1':
            discount = total_price_decimal * Decimal('0.50')
        elif promo_code == 'SAVE50':
            discount = Decimal('50.00')
        
        final_price = total_price_decimal - discount
        if final_price < Decimal('0.00'):
            final_price = Decimal('0.00')
        
        rest_name = "Unknown Restaurant"
        for rest in RESTAURANT_LIST_DATA:
            if str(rest['id']) == str(rest_id):
                rest_name = rest['name']
                break
        
        Order.objects.create(
            user=request.user,
            restaurant_name=rest_name,
            items=items,
            total_price=final_price,
            status='Pending'
        )
        return redirect('core:my_orders')
    return redirect('core:near_me')