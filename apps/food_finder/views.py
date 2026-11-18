import copy
import json
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.staticfiles import finders
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import escape
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from .models import Restaurant, Review


# ============================================================
# FOOD DATA
# ============================================================
FOOD_DATA = {
    "fastfood": [
        {
            "name": "【entity-Jollibee¦canonical_name=Jollibee】 (Guanzon)",
            "mapQuery": "【entity-Jollibee¦canonical_name=Jollibee】 Guanzon St, Kabankalan City",
            "rating": "4.5",
            "price": "₱50–₱250",
            "img": "https://commons.wikimedia.org/wiki/Special:FilePath/Jollibee_branch_(bagong_silang,_caloocan)(2015-08-23).jpg?width=800",
            "address": "Guanzon St, Kabankalan City Proper",
            "menu": [
                {"name": "1-pc. Breakfast Chickenjoy Solo", "price": "₱99", "desc": "Crispy fried chicken with garlic rice and egg"},
                {"name": "1-pc. Breakfast Chickenjoy w/ Drink", "price": "₱120", "desc": "Breakfast Chickenjoy with regular drink"},
                {"name": "Longganisa Solo", "price": "₱85", "desc": "Garlic rice, fried egg, and 2 pieces longganisa"},
                {"name": "Beef Tapa Solo", "price": "₱95", "desc": "Garlic rice, fried egg, and tender beef tapa"},
                {"name": "Corned Beef Solo", "price": "₱85", "desc": "Garlic rice, fried egg, and juicy corned beef"},
                {"name": "Breakfast Burger Steak Solo", "price": "₱89", "desc": "Garlic rice, fried egg, and gravy-poured steak"},
                {"name": "Breakfast Hotdog Solo", "price": "₱75", "desc": "Garlic rice, fried egg, and meaty hotdog"},
                {"name": "2-pc. Pancakes Solo", "price": "₱75", "desc": "Moist pancakes with butter and maple syrup"},
                {"name": "Bacon, Egg, & Cheese Pancake Sandwich Solo", "price": "₱95", "desc": "Crispy bacon, cheese, and egg in pancake buns"},
                {"name": "Hot Chocolate", "price": "₱45", "desc": "Warm hot chocolate drink"},
                {"name": "Hot Fresh Brew", "price": "₱40", "desc": "Freshly brewed coffee"},
            ],
        },
        {
            "name": "McDonald's (Guanzon)",
            "mapQuery": "McDonalds Guanzon St, Kabankalan City",
            "rating": "4.3",
            "price": "₱50–₱650",
            "img": "/static/images/mcdonalds.jpg",
            "address": "Guanzon St, Kabankalan City Proper",
            "menu": [
                {"name": "Big Mac", "price": "₱209", "desc": "Double-decker burger"},
                {"name": "Quarter Pounder with Cheese", "price": "₱209", "desc": "Quarter pound beef with cheese"},
                {"name": "Double Cheeseburger", "price": "₱161", "desc": "Double patty with cheese"},
                {"name": "Cheeseburger", "price": "₱104", "desc": "Classic cheeseburger"},
                {"name": "Burger McDo", "price": "₱55", "desc": "Classic burger"},
                {"name": "McSpicy", "price": "₱227", "desc": "Spicy chicken burger"},
                {"name": "1-pc. Chicken McDo", "price": "₱104", "desc": "Crispy fried chicken"},
                {"name": "2-pc. Chicken McDo", "price": "₱197", "desc": "Two-piece fried chicken"},
                {"name": "McSpaghetti", "price": "₱82", "desc": "Sweet-style spaghetti"},
                {"name": "Regular Fries", "price": "₱74", "desc": "Golden french fries"},
                {"name": "Medium Fries", "price": "₱100", "desc": "Medium french fries"},
                {"name": "Large Fries", "price": "₱120", "desc": "Large french fries"},
                {"name": "McFlurry with Oreo", "price": "₱79", "desc": "Oreo ice cream dessert"},
                {"name": "Hot Fudge Sundae", "price": "₱62", "desc": "Vanilla sundae with fudge"},
                {"name": "Coke Medium", "price": "₱77", "desc": "Medium Coke"},
                {"name": "McCafé Iced Coffee Original Medium", "price": "₱68", "desc": "Creamy iced coffee"},
            ],
        },
        {
            "name": "Mang Inasal (Gaisano)",
            "mapQuery": "Mang Inasal Gaisano Grand Mall Kabankalan",
            "rating": "4.4",
            "price": "₱50–₱1,175",
            "img": "/static/images/mang-inasal.jpg",
            "address": "Gaisano Grand Mall, City Proper",
            "menu": [
                {"name": "Paa Large 1 Rice", "price": "₱139", "desc": "Chicken inasal leg with rice"},
                {"name": "Paa Large Unli Rice", "price": "₱179", "desc": "Chicken inasal leg with unlimited rice"},
                {"name": "Pecho Large 1 Rice", "price": "₱169", "desc": "Chicken inasal breast with rice"},
                {"name": "Pecho Large Unli Rice", "price": "₱209", "desc": "Chicken inasal breast with unlimited rice"},
                {"name": "Regular Chicken 1 Rice", "price": "₱99", "desc": "Regular chicken inasal with rice"},
                {"name": "Regular Chicken Unli Rice", "price": "₱139", "desc": "Regular chicken inasal with unlimited rice"},
                {"name": "1pc Pork BBQ Ala Carte", "price": "₱50", "desc": "Grilled pork skewer"},
                {"name": "2pc Pork BBQ Value Meal", "price": "₱134", "desc": "Two pork BBQ with rice and drink"},
                {"name": "Liempo Inasal 1 Rice", "price": "₱135", "desc": "Grilled liempo with rice"},
                {"name": "Pork Sisig 1 Rice", "price": "₱105", "desc": "Sizzling pork sisig with rice"},
                {"name": "Bangus Sisig 1 Rice", "price": "₱135", "desc": "Milkfish sisig with rice"},
                {"name": "Halo-Halo Extra Creamy 8oz", "price": "₱39", "desc": "Extra creamy halo-halo"},
                {"name": "Halo-Halo 12oz Small", "price": "₱75", "desc": "Small halo-halo"},
                {"name": "Halo-Halo 16oz Regular", "price": "₱95", "desc": "Regular halo-halo"},
                {"name": "Palabok Solo", "price": "₱89", "desc": "Palabok noodles"},
            ],
        },
        {
            "name": "Chowking (City Mall)",
            "mapQuery": "Chowking CityMall Kabankalan",
            "rating": "4.1",
            "price": "₱18–₱1,474",
            "img": "https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=800&auto=format&fit=crop",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Chao Fan", "price": "₱92", "desc": "Fried rice with toppings"},
                {"name": "Spicy Chao Fan", "price": "₱92", "desc": "Spicy fried rice with pork and kangkong"},
                {"name": "Beef Chao Fan", "price": "₱116", "desc": "Beefy fried rice"},
                {"name": "Wonton Mami Regular", "price": "₱116", "desc": "Noodle soup with wonton"},
                {"name": "Beef Mami Large", "price": "₱221", "desc": "Beef noodle soup"},
                {"name": "Pancit Canton", "price": "₱99", "desc": "Stir-fried noodles"},
                {"name": "Chunky Asado Siopao", "price": "₱64", "desc": "Steamed bun with asado filling"},
                {"name": "4pc Lumpiang Shanghai", "price": "₱92", "desc": "Deep-fried spring rolls"},
                {"name": "6pc Spicy Wonton", "price": "₱92", "desc": "Spicy wonton dumplings"},
                {"name": "3pc Buchi", "price": "₱92", "desc": "Sesame rice balls with lotus cream"},
                {"name": "Chicharap with Spicy Vinegar", "price": "₱92", "desc": "Crispy prawn crackers"},
                {"name": "Halo-Halo Supreme Medium", "price": "₱116", "desc": "Loaded halo-halo with ice cream"},
                {"name": "Chinese-Style Fried Chicken Lauriat", "price": "₱233", "desc": "Chicken with rice, pancit, siomai, chicharap, buchi"},
            ],
        },
        {
            "name": "Angel's Burger (Rizal)",
            "mapQuery": "Angels Burger Rizal St, Kabankalan City",
            "rating": "4.2",
            "price": "₱25–₱60",
            "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Burger Steak", "price": "₱35", "desc": "Classic burger"},
                {"name": "Cheese Burger", "price": "₱45", "desc": "Burger with cheese"},
                {"name": "Hotdog Sandwich", "price": "₱30", "desc": "Hotdog in a bun"},
            ],
        },
        {
            "name": "Lola Nena's Lomi",
            "mapQuery": "Lola Nenas Lomi Tan Lorenzo Kabankalan",
            "rating": "4.7",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=800&auto=format&fit=crop",
            "address": "Tan Lorenzo St, City Proper",
            "menu": [
                {"name": "Special Lomi", "price": "₱90", "desc": "Noodle soup"},
                {"name": "Pancit Canton", "price": "₱85", "desc": "Stir-fried noodles"},
                {"name": "Batchoy", "price": "₱85", "desc": "Pork noodle soup"},
            ],
        },
        {
            "name": "Greenwich (City Mall)",
            "mapQuery": "Greenwich CityMall Kabankalan",
            "rating": "4.3",
            "price": "₱100–₱250",
            "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=800&auto=format&fit=crop",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Hawaiian Overload", "price": "₱199", "desc": "Pizza"},
                {"name": "Carbonara", "price": "₱150", "desc": "Creamy pasta"},
                {"name": "Chicken Alfredo", "price": "₱160", "desc": "Pasta with chicken"},
            ],
        },
        {
            "name": "KFC (Gaisano)",
            "mapQuery": "KFC Gaisano Grand Mall Kabankalan",
            "rating": "4.2",
            "price": "₱30–₱1,575",
            "img": "https://images.unsplash.com/photo-1562967914-608f82629710?q=80&w=800&auto=format&fit=crop",
            "address": "Gaisano Grand Mall, City Proper",
            "menu": [
                {"name": "1-PC Chicken Ala Carte", "price": "₱115", "desc": "Crispy fried chicken"},
                {"name": "2-PC Chicken Ala Carte", "price": "₱220", "desc": "Two-piece fried chicken"},
                {"name": "1-PC Chicken Meal", "price": "₱140", "desc": "Chicken with rice and drink"},
                {"name": "Zinger Burger", "price": "₱195", "desc": "Spicy chicken burger"},
                {"name": "Chicken Burger", "price": "₱75", "desc": "Classic chicken burger"},
                {"name": "Spaghetti", "price": "₱85", "desc": "Sweet-style spaghetti"},
                {"name": "Bucket Of 6", "price": "₱595", "desc": "6 pieces fried chicken"},
                {"name": "Bucket Of 8", "price": "₱765", "desc": "8 pieces fried chicken"},
                {"name": "Crispy Fries", "price": "₱80", "desc": "Crispy french fries"},
                {"name": "Mashed Potato Regular", "price": "₱65", "desc": "Creamy mashed potato"},
            ],
        },
        {
            "name": "Snackee (Mabini/Rizal)",
            "mapQuery": "Snackee Mabini Rizal Kabankalan",
            "rating": "4.5",
            "price": "₱78–₱219",
            "img": "https://images.unsplash.com/photo-1562967914-608f82629710?q=80&w=800&auto=format&fit=crop",
            "address": "Mabini St. corner Rizal St., City Proper",
            "menu": [
                {"name": "Honey Glazed Fried Chicken", "price": "₱168", "desc": "Crispy honey-glazed fried chicken"},
                {"name": "Honey Glazed With Iced Tea", "price": "₱203", "desc": "Honey glazed chicken with iced tea"},
                {"name": "Garlicky Fried Chicken", "price": "₱166", "desc": "Crispy garlic-flavored chicken"},
                {"name": "Garlicky With Iced Tea", "price": "₱201", "desc": "Garlicky chicken with iced tea"},
                {"name": "Spicy With Iced Tea", "price": "₱201", "desc": "Spicy fried chicken with iced tea"},
                {"name": "Buttered With Iced Tea", "price": "₱201", "desc": "Buttered fried chicken with iced tea"},
                {"name": "Classic Fried Chicken", "price": "₱155", "desc": "Traditional fried chicken"},
                {"name": "Classic With Iced Tea", "price": "₱190", "desc": "Classic fried chicken with iced tea"},
                {"name": "Classic Loaded", "price": "₱219", "desc": "Loaded fried chicken with sides"},
                {"name": "Classic Chicken Burger", "price": "₱78", "desc": "Juicy classic chicken burger"},
                {"name": "Garlicky Chicken Burger", "price": "₱84", "desc": "Chicken burger with garlic sauce"},
                {"name": "Buttered Chicken Burger", "price": "₱84", "desc": "Chicken burger with creamy sauce"},
                {"name": "Chicken Lomi Family", "price": "₱216", "desc": "Hearty chicken noodle soup for sharing"},
                {"name": "Halo-Halo Regular", "price": "₱102", "desc": "Shaved ice dessert"},
                {"name": "Mango Graham Halo-halo", "price": "₱150", "desc": "Fruity, creamy, icy dessert"},
                {"name": "Iced Coffee", "price": "₱90", "desc": "Refreshing iced coffee"},
                {"name": "Houseblend Iced Tea XL", "price": "₱105", "desc": "Large houseblend iced tea"},
            ],
        },
    ],
    "grillhouse": [
        {
            "name": "Rosalino's Chicken Inasal and Seafood",
            "mapQuery": "Kabankalan Ihaw-Ihaw Rizal St",
            "rating": "4.5",
            "price": "₱1–₱500",
            "hours": "Open daily, 10:00 AM – 8:30 PM",
            "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?q=80&w=800&auto=format&fit=crop",
            "address": "Near the city center (XRW7+79M), Kabankalan City",
            "menu": [
                {"name": "Pork BBQ", "price": "₱100", "desc": "Grilled skewers"},
                {"name": "Chicken BBQ", "price": "₱120", "desc": "Grilled chicken skewers"},
                {"name": "Isaw", "price": "₱30", "desc": "Grilled chicken intestine"},
                {"name": "Puso (Hanging Rice)", "price": "₱15", "desc": "Rice wrapped in coconut leaves"},
            ],
        },
        {
            "name": "MG's Grill House Kabankalan",
            "mapQuery": "MGs Grill House Aquiles Zayco Avenue Kabankalan",
            "rating": "4.5",
            "price": "₱50–₱300",
            "hours": "Open daily, 9:00 AM – 9:00 PM",
            "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=800&auto=format&fit=crop",
            "address": "Aquiles - Zayco Avenue, Barangay 4, Kabankalan City",
            "menu": [
                {"name": "Chicken Inasal", "price": "₱100", "desc": "Budget-friendly grilled chicken inasal with rice"},
                {"name": "Grilled Platter", "price": "₱150", "desc": "Grilled platter served with rice"},
            ],
        },
        {
            "name": "Amore Mio Pizza & Inasal",
            "mapQuery": "Amore Mio Pizza Rizal Kabankalan",
            "rating": "4.3",
            "price": "₱1–₱500",
            "hours": "Wed & Fri–Tue 12:00 PM – 8:30 PM (closed Thursdays)",
            "img": "/static/images/amore_mio.webp",
            "address": "SNC Building, Rizal Street, Barangay 9, Kabankalan City",
            "menu": [
                {"name": "Margherita", "price": "₱299", "desc": "Italian pizza"},
                {"name": "Pepperoni", "price": "₱320", "desc": "Pepperoni pizza"},
                {"name": "Four Cheese", "price": "₱350", "desc": "Cheese pizza"},
                {"name": "Pasta", "price": "Ask in store", "desc": "Italian-style pasta"},
                {"name": "Chicken Inasal", "price": "Ask in store", "desc": "Grilled chicken inasal with rice"},
            ],
        },
    ],
    "carinderia": [
        {
            "name": "ALONSO's Cansi",
            "mapQuery": "Alonsos Cansi Guanzon Kabankalan",
            "rating": "4.8",
            "price": "₱150–₱300",
            "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, Brgy. 1, City Proper",
            "menu": [
                {"name": "Special Cansi", "price": "₱130", "desc": "Sour beef soup"},
                {"name": "Cansi Bulalo", "price": "₱250", "desc": "Rich beef marrow soup"},
                {"name": "Pork BBQ", "price": "₱100", "desc": "Grilled pork skewers"},
            ],
        },
        {
            "name": "Cansi House",
            "mapQuery": "Cansi House Rizal Kabankalan",
            "rating": "4.7",
            "price": "₱120–₱280",
            "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, Brgy. 5, City Proper",
            "menu": [
                {"name": "Cansi Bulalo", "price": "₱280", "desc": "Rich soup"},
                {"name": "Special Cansi", "price": "₱150", "desc": "Sour beef soup"},
                {"name": "Cansi with Saging", "price": "₱160", "desc": "Cansi with banana"},
            ],
        },
        {
            "name": "Sharyn's Cansi",
            "mapQuery": "Sharyns Cansi National Highway Kabankalan",
            "rating": "4.6",
            "price": "₱150–₱260",
            "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=800&auto=format&fit=crop",
            "address": "National Highway, Brgy. 1, City Proper",
            "menu": [
                {"name": "Special Cansi", "price": "₱260", "desc": "Sour soup"},
                {"name": "Cansi Regular", "price": "₱180", "desc": "Regular cansi"},
            ],
        },
        {
            "name": "Aida's Carinderia",
            "mapQuery": "Aidas Carinderia Public Market Kabankalan",
            "rating": "4.5",
            "price": "₱50–₱100",
            "img": "https://images.unsplash.com/photo-1552566626-52f8b828add9?q=80&w=800&auto=format&fit=crop",
            "address": "Public Market, City Proper",
            "menu": [
                {"name": "Adobo with Rice", "price": "₱70", "desc": "Classic adobo"},
                {"name": "Sinigang na Baboy", "price": "₱85", "desc": "Sour pork soup"},
                {"name": "Fried Fish with Rice", "price": "₱75", "desc": "Crispy fried fish"},
            ],
        },
        {
            "name": "Tita Beth's Eatery",
            "mapQuery": "Tita Beths Eatery Guanzon Kabankalan",
            "rating": "4.6",
            "price": "₱60–₱120",
            "img": "https://images.unsplash.com/photo-1552566626-52f8b828add9?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St., Brgy. 2, City Proper",
            "menu": [
                {"name": "Kare-Kare", "price": "₱120", "desc": "Peanut stew"},
                {"name": "Pork Adobo", "price": "₱85", "desc": "Home-cooked adobo"},
                {"name": "Sinigang na Hipon", "price": "₱100", "desc": "Shrimp sour soup"},
            ],
        },
        {
            "name": "Myrna's Restaurant",
            "mapQuery": "Myrnas Restaurant Tan Lorenzo Kabankalan",
            "rating": "4.4",
            "price": "₱80–₱150",
            "hours": "Open daily, 6:00 AM – 3:30 PM (cash only)",
            "img": "/static/images/myrnas.jpg",
            "address": "Tan Lorenzo Street, Kabankalan City, Negros Occidental",
            "menu": [
                {"name": "Pork Adobo", "price": "₱85", "desc": "Home-cooked"},
                {"name": "Chicken Inasal", "price": "₱110", "desc": "Grilled chicken"},
                {"name": "Pancit Bihon", "price": "₱80", "desc": "Rice noodles"},
            ],
        },
        {
            "name": "3RD Talabahan",
            "mapQuery": "3RD Talabahan Lirazan Kabankalan",
            "rating": "4.5",
            "price": "₱100–₱250",
            "hours": "Open daily, 9:00 AM – 9:30 PM",
            "img": "/static/images/3rd_talabahan.webp",
            "address": "Lirazan Street, Kabankalan City, Negros Occidental",
            "menu": [
                {"name": "Baked Talaba", "price": "₱150", "desc": "Fresh oysters"},
                {"name": "Grilled Talaba", "price": "₱120", "desc": "Grilled oysters"},
                {"name": "Kilawin na Talaba", "price": "₱130", "desc": "Fresh oyster ceviche"},
                {"name": "Mixed Seafood", "price": "Ask in store", "desc": "Assorted fresh seafood"},
            ],
        },
        {
            "name": "Cansi ni Tatay Andoy",
            "mapQuery": "Cansi ni Tatay Andoy Kabankalan",
            "rating": "4.7",
            "price": "₱100–₱220",
            "img": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, Brgy. 3, City Proper",
            "menu": [
                {"name": "Cansi Special", "price": "₱120", "desc": "Batwan-soured beef soup"},
                {"name": "Cansi Bulalo", "price": "₱200", "desc": "Rich beef marrow cansi"},
            ],
        },
        {
            "name": "Nena's Cansi Hauz",
            "mapQuery": "Nenas Cansi Hauz Kabankalan",
            "rating": "4.6",
            "price": "₱120–₱250",
            "img": "https://images.unsplash.com/photo-1445116572660-236099ec97a0?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, Brgy. 4, City Proper",
            "menu": [
                {"name": "Cansi with Saging", "price": "₱140", "desc": "Cansi with banana"},
                {"name": "Special Cansi", "price": "₱130", "desc": "Sour beef soup"},
            ],
        },
        {
            "name": "Pares King Kabankalan",
            "mapQuery": "Pares King Kabankalan",
            "rating": "4.5",
            "price": "₱60–₱120",
            "img": "https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=800&auto=format&fit=crop",
            "address": "Araneta St, City Proper",
            "menu": [
                {"name": "Beef Pares", "price": "₱80", "desc": "Sweet-savory beef stew"},
                {"name": "Pares with Rice", "price": "₱95", "desc": "Beef pares with rice"},
                {"name": "Pares Mami", "price": "₱90", "desc": "Pares noodle soup"},
            ],
        },
        {
            "name": "Castaño's Dine and Drink",
            "mapQuery": "Castanos Dine and Drink Kabankalan",
            "rating": "4.5",
            "price": "₱80–₱250",
            "img": "/static/images/castanos.jpg",
            "address": "G. Cordova Street, Kabankalan City, Negros Occidental",
            "menu": [
                {"name": "Chicken Inasal + Belly + Unli Rice + Coke", "price": "₱220", "desc": "Sulit meal combo"},
                {"name": "Lechon Belly", "price": "Package starts ₱4,900", "desc": "Original Lechon Belly of Kabankalan (pre-order)"},
                {"name": "Belly + Dinuguan + Fish Tinola", "price": "Unli Rice meal", "desc": "Warm meal set"},
                {"name": "Shrimp and Prawn Dishes", "price": "Ask in store", "desc": "Seafood dishes, dine-in or takeout"},
            ],
        },
        {
            "name": "Café CHIKO",
            "mapQuery": "Cafe CHIKO Aquiles Zayco Kabankalan",
            "rating": "4.4",
            "price": "₱70–₱150",
            "img": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?q=80&w=800&auto=format&fit=crop",
            "address": "Aquiles/Obi Zayco Avenue, City Proper",
            "menu": [
                {"name": "KBL (Kadyos, Baboy, Langka)", "price": "₱90", "desc": "Ilonggo sour soup"},
                {"name": "Kilawin", "price": "₱100", "desc": "Fresh fish ceviche"},
                {"name": "Ginataan nga Langka", "price": "₱80", "desc": "Jackfruit in coconut milk"},
                {"name": "Chicken Adobo with Pineapples", "price": "₱90", "desc": "Adobo with pineapple chunks"},
                {"name": "Humba", "price": "₱95", "desc": "Sweet-savory braised pork"},
            ],
        },
        {
            "name": "Emilio's Bistro",
            "mapQuery": "Emilios Bistro Rizal Kabankalan",
            "rating": "4.4",
            "price": "₱150–₱350",
            "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop",
            "address": "#64 Rizal St., City Proper",
            "menu": [
                {"name": "Adobo sa Gata (Chicken/Pork)", "price": "₱180", "desc": "Adobo in rich coconut milk"},
                {"name": "Garlic Fried Rice", "price": "₱60", "desc": "Perfect pair for Adobo sa Gata"},
            ],
        },
        {
            "name": "Reegal's Refreshment",
            "mapQuery": "Reegals Refreshment Kabankalan",
            "rating": "4.3",
            "price": "₱1–₱500",
            "img": "/static/images/reegals.webp",
            "address": "Rizal Street (near the Kabankalan City Public Plaza), Barangay 7, Kabankalan City, Negros Occidental",
            "menu": [
                {"name": "Super Special Batchoy", "price": "₱85", "desc": "Known for their batchoy"},
                {"name": "Pancit Canton", "price": "₱75", "desc": "Stir-fried noodles"},
                {"name": "Halo-Halo", "price": "Ask in store", "desc": "Shaved ice dessert"},
                {"name": "Cakes and Pastries", "price": "Ask in store", "desc": "Assorted cakes and pastries"},
                {"name": "Siopao", "price": "Ask in store", "desc": "Steamed bun with filling"},
                {"name": "Silog Breakfast Meal", "price": "Ask in store", "desc": "Garlic rice, fried egg, and choice of meat"},
            ],
        },
    ],
    "cafe": [
        {
            "name": "Gorio's Cafe",
            "mapQuery": "Gorios Cafe Guanzon Kabankalan",
            "rating": "4.9",
            "price": "₱100–₱250",
            "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, Kabankalan City Proper",
            "menu": [
                {"name": "Iced Latte", "price": "₱120", "desc": "Espresso and milk"},
                {"name": "Cappuccino", "price": "₱110", "desc": "Espresso with milk foam"},
                {"name": "Caramel Macchiato", "price": "₱130", "desc": "Sweet caramel coffee"},
            ],
        },
        {
            "name": "Taza La Bien",
            "mapQuery": "Taza La Bien Los Angeles Kabankalan",
            "rating": "4.8",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=800&auto=format&fit=crop",
            "address": "Los Angeles St, Brgy. 1, City Proper",
            "menu": [
                {"name": "Caffe Latte", "price": "₱120", "desc": "Steamed milk"},
                {"name": "Americano", "price": "₱90", "desc": "Black coffee"},
                {"name": "Spanish Latte", "price": "₱130", "desc": "Sweet espresso drink"},
            ],
        },
        {
            "name": "Kalamay Artisan Patisserie & Cafe",
            "mapQuery": "Kalamay Artisan Lirazan Kabankalan",
            "rating": "4.4",
            "price": "₱1–₱500",
            "hours": "Mon–Thu 8:30 AM – 7:30 PM; Fri–Sun 7:30 AM – 7:30 PM",
            "img": "/static/images/kalamay.webp",
            "address": "42 Lirazan Street, Barangay 4, Kabankalan City",
            "menu": [
                {"name": "Cappuccino", "price": "₱110", "desc": "Milk foam"},
                {"name": "Matcha Latte", "price": "₱130", "desc": "Green tea latte"},
                {"name": "Chocolate Cake", "price": "₱120", "desc": "Chocolate slice"},
                {"name": "British Dish", "price": "Ask in store", "desc": "British-inspired main dish"},
                {"name": "European Bread", "price": "Ask in store", "desc": "Freshly baked European-style bread"},
            ],
        },
        {
            "name": "Kapehan sa Plaza",
            "mapQuery": "Kapehan sa Plaza Kabankalan",
            "rating": "4.5",
            "price": "₱30–₱100",
            "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=800&auto=format&fit=crop",
            "address": "Plaza Area, Brgy. 1, City Proper",
            "menu": [
                {"name": "Native Coffee", "price": "₱30", "desc": "Brewed coffee"},
                {"name": "3-in-1 Coffee", "price": "₱40", "desc": "Instant coffee"},
            ],
        },
        {
            "name": "MOICA Pizzeria",
            "mapQuery": "MOICA Pizzeria Coloso Kabankalan",
            "rating": "4.7",
            "price": "₱150–₱400",
            "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=800&auto=format&fit=crop",
            "address": "Coloso St, Brgy. 6, City Proper",
            "menu": [
                {"name": "Pepperoni Pizza", "price": "₱350", "desc": "Classic pizza"},
                {"name": "Margherita Pizza", "price": "₱299", "desc": "Italian pizza"},
                {"name": "Carbonara", "price": "₱180", "desc": "Creamy pasta"},
            ],
        },
        {
            "name": "Bo's Coffee (CityMall)",
            "mapQuery": "Bos Coffee CityMall Kabankalan",
            "rating": "4.4",
            "price": "₱100–₱180",
            "img": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?q=80&w=800&auto=format&fit=crop",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Brewed Coffee", "price": "₱100", "desc": "Local beans"},
                {"name": "Iced Americano", "price": "₱120", "desc": "Iced black coffee"},
                {"name": "Cheesecake", "price": "₱150", "desc": "Creamy cheesecake slice"},
            ],
        },
        {
            "name": "Sagay Cafe Kabankalan",
            "mapQuery": "Sagay Cafe Guanzon Kabankalan",
            "rating": "4.5",
            "price": "₱80–₱180",
            "img": "https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?q=80&w=800&auto=format&fit=crop",
            "address": "Guanzon St, City Proper",
            "menu": [
                {"name": "Spanish Latte", "price": "₱110", "desc": "Sweet espresso drink"},
                {"name": "Iced Matcha", "price": "₱120", "desc": "Green tea latte"},
            ],
        },
        {
            "name": "The Coffee Project",
            "mapQuery": "The Coffee Project Rizal Kabankalan",
            "rating": "4.4",
            "price": "₱90–₱200",
            "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Caramel Macchiato", "price": "₱130", "desc": "Sweet caramel coffee"},
                {"name": "Mocha Frappe", "price": "₱150", "desc": "Blended mocha drink"},
            ],
        },
        {
            "name": "Kape Centrale",
            "mapQuery": "Kape Centrale Punta Guanzon Kabankalan",
            "rating": "4.5",
            "price": "₱100–₱400",
            "img": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=800&auto=format&fit=crop",
            "address": "Punta, Guanzon St., City Proper (near Public Plaza)",
            "menu": [
                {"name": "Squid Ink Pasta", "price": "₱280", "desc": "Standout pasta dish"},
                {"name": "Pork Steak", "price": "₱250", "desc": "Customer favorite"},
                {"name": "Tuna Melt", "price": "₱180", "desc": "Sandwich melt"},
                {"name": "Strawberry Smoothie", "price": "₱150", "desc": "Fresh fruit smoothie"},
                {"name": "Iced Coffee", "price": "₱120", "desc": "Beautifully presented iced coffee"},
            ],
        },
        {
            "name": "MOÍCA Pizzeria & Bar",
            "mapQuery": "MOICA Pizzeria Cordero Kabankalan",
            "rating": "4.7",
            "price": "₱200–₱500",
            "img": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?q=80&w=800&auto=format&fit=crop",
            "address": "Cordero St., Brgy. 4, City Proper (in front of Kabankalan National High School)",
            "menu": [
                {"name": "Brick Oven Pizza", "price": "₱350–₱500", "desc": "Authentic Italian pizza, oven built by owner"},
                {"name": "Pasta in a Bowl", "price": "₱250", "desc": "Italian pasta"},
                {"name": "Focaccia Bread", "price": "₱150", "desc": "Italian flatbread"},
                {"name": "Bruschetta", "price": "₱150", "desc": "Toasted bread with toppings"},
                {"name": "Ice-cold Lemonade", "price": "₱80", "desc": "Refreshing drink"},
            ],
        },
    ],
    "desserts": [
        {
            "name": "Cake Avenue",
            "mapQuery": "Cake Avenue Rizal Kabankalan",
            "rating": "4.7",
            "price": "₱80–₱150",
            "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Chocolate Cake", "price": "₱120", "desc": "Chocolate slice"},
                {"name": "Red Velvet Cake", "price": "₱130", "desc": "Red velvet slice"},
                {"name": "Cheesecake", "price": "₱140", "desc": "Creamy cheesecake"},
            ],
        },
        {
            "name": "Melting Pot",
            "mapQuery": "Melting Pot Rizal Kabankalan",
            "rating": "4.4",
            "price": "₱55–₱165",
            "img": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?q=80&w=800&auto=format&fit=crop",
            "address": "Rizal St, Brgy. 7, City Proper",
            "menu": [
                {"name": "Sundae", "price": "₱55", "desc": "Ice cream"},
                {"name": "Halo-Halo", "price": "₱99", "desc": "Shaved ice dessert"},
                {"name": "Banana Split", "price": "₱120", "desc": "Banana with ice cream"},
            ],
        },
        {
            "name": "Bibingka Station",
            "mapQuery": "Bibingka Station Church Kabankalan",
            "rating": "4.9",
            "price": "₱40–₱100",
            "img": "/static/images/bibingka-station.jpg",
            "address": "Church Vicinity, City Proper",
            "menu": [
                {"name": "Bibingka", "price": "₱50", "desc": "Rice cake"},
                {"name": "Puto Bumbong", "price": "₱60", "desc": "Purple rice cake"},
            ],
        },
        {
            "name": "Leche Flan ni Aling Rosa",
            "mapQuery": "Leche Flan Public Market Kabankalan",
            "rating": "4.8",
            "price": "₱60–₱120",
            "img": "/static/images/leche-flan-ni-aling.jpg",
            "address": "Public Market, City Proper",
            "menu": [
                {"name": "Leche Flan", "price": "₱70", "desc": "Caramel custard"},
                {"name": "Leche Flan (Large)", "price": "₱120", "desc": "Large caramel custard"},
            ],
        },
        {
            "name": "Don Benito's",
            "mapQuery": "Don Benitos Guanzon Kabankalan",
            "rating": "4.5",
            "price": "₱80–₱150",
            "img": "/static/images/don-benitos.jpg",
            "address": "Guanzon St, City Proper",
            "menu": [
                {"name": "Halo-Halo", "price": "₱99", "desc": "Shaved ice dessert"},
                {"name": "Mais con Yelo", "price": "₱85", "desc": "Sweet corn with ice"},
            ],
        },
        {
            "name": "Red Ribbon (CityMall)",
            "mapQuery": "Red Ribbon CityMall Kabankalan",
            "rating": "4.6",
            "price": "₱100–₱200",
            "img": "/static/images/red-ribbon.jpg",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Black Forest", "price": "₱120", "desc": "Cake slice"},
                {"name": "Chocolate Mousse", "price": "₱130", "desc": "Chocolate mousse cake"},
                {"name": "Mango Cake", "price": "₱140", "desc": "Mango cake slice"},
            ],
        },
        {
            "name": "Halo-Halo sa Plaza",
            "mapQuery": "Halo-Halo Plaza Kabankalan",
            "rating": "4.6",
            "price": "₱50–₱100",
            "img": "/static/images/halo-halo-sa-plaza.jpg",
            "address": "Plaza Area, City Proper",
            "menu": [
                {"name": "Special Halo-Halo", "price": "₱85", "desc": "Loaded shaved ice dessert"},
                {"name": "Halo-Halo Regular", "price": "₱60", "desc": "Regular halo-halo"},
            ],
        },
        {
            "name": "Sweet Corner Bakeshop",
            "mapQuery": "Sweet Corner Bakeshop Guanzon Kabankalan",
            "rating": "4.5",
            "price": "₱40–₱120",
            "img": "/static/images/sweet-corner-bakery.jpg",
            "address": "Guanzon St, City Proper",
            "menu": [
                {"name": "Mango Graham", "price": "₱90", "desc": "Layered mango dessert"},
                {"name": "Graham Cake", "price": "₱80", "desc": "Graham cake slice"},
            ],
        },
        {
            "name": "Puto Pao Master",
            "mapQuery": "Puto Pao Master Villa San Jose Kabankalan",
            "rating": "4.5",
            "price": "₱20–₱60",
            "img": "/static/images/puto-pao-master.jpg",
            "address": "Villa San Jose Subdivision, Brgy. 6, City Proper",
            "menu": [
                {"name": "Puto Pao", "price": "₱25", "desc": "Steamed rice cake with filling"},
                {"name": "Puto", "price": "₱15", "desc": "Traditional steamed rice cake"},
            ],
        },
    ],
    "milktea": [
        {
            "name": "Chatime (City Mall)",
            "mapQuery": "Chatime CityMall Kabankalan",
            "rating": "4.8",
            "price": "₱70–₱140",
            "img": "/static/images/chatime.jpg",
            "address": "City Mall, City Proper",
            "menu": [
                {"name": "Pearl Milk Tea", "price": "₱85", "desc": "Classic pearls"},
                {"name": "Grass Jelly Milk Tea", "price": "₱90", "desc": "With grass jelly"},
                {"name": "Taro Milk Tea", "price": "₱95", "desc": "Taro-flavored milk tea"},
            ],
        },
        {
            "name": "Macao Imperial Tea",
            "mapQuery": "Macao Imperial Tea Gaisano Kabankalan",
            "rating": "4.6",
            "price": "₱90–₱160",
            "img": "/static/images/macao.jpg",
            "address": "Gaisano Grand Mall, City Proper",
            "menu": [
                {"name": "Cream Cheese", "price": "₱120", "desc": "Cheesecake series"},
                {"name": "Brown Sugar Milk Tea", "price": "₱110", "desc": "Brown sugar pearls"},
            ],
        },
        {
            "name": "CoCo Fresh Tea",
            "mapQuery": "CoCo Fresh Tea Araneta Kabankalan",
            "rating": "4.5",
            "price": "₱90–₱130",
            "img": "/static/images/coco.jpg",
            "address": "Araneta St, City Proper",
            "menu": [
                {"name": "3Q Milk Tea", "price": "₱110", "desc": "Pearl, pudding, jelly"},
                {"name": "Pearl Milk Tea", "price": "₱95", "desc": "Classic pearl milk tea"},
            ],
        },
        {
            "name": "SereniTea",
            "mapQuery": "SereniTea Rizal Kabankalan",
            "rating": "4.4",
            "price": "₱70–₱120",
            "img": "/static/images/serenitea.jpg",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Wintermelon", "price": "₱75", "desc": "Sweet and refreshing"},
                {"name": "Okinawa", "price": "₱85", "desc": "Brown sugar milk tea"},
            ],
        },
        {
            "name": "Tea Talk",
            "mapQuery": "Tea Talk Guanzon Kabankalan",
            "rating": "4.3",
            "price": "₱60–₱100",
            "img": "/static/images/tea-talk.jpg",
            "address": "Guanzon St, City Proper",
            "menu": [
                {"name": "Okinawa", "price": "₱85", "desc": "Brown sugar milk tea"},
                {"name": "Wintermelon", "price": "₱75", "desc": "Sweet wintermelon milk tea"},
                {"name": "Hokkaido", "price": "₱85", "desc": "Creamy Hokkaido milk tea"},
            ],
        },
        {
            "name": "Infinitea",
            "mapQuery": "Infinitea Kabankalan",
            "rating": "4.5",
            "price": "₱80–₱130",
            "img": "/static/images/infinitea.jpg",
            "address": "City Proper, Kabankalan",
            "menu": [
                {"name": "Hokkaido", "price": "₱95", "desc": "Creamy milk tea"},
                {"name": "Wintermelon", "price": "₱85", "desc": "Sweet wintermelon"},
            ],
        },
        {
            "name": "Dakasi (CityMall)",
            "mapQuery": "Dakasi CityMall Kabankalan",
            "rating": "4.5",
            "price": "₱70–₱130",
            "img": "/static/images/dakasi.jpg",
            "address": "CityMall, City Proper",
            "menu": [
                {"name": "Cheesecake Milk Tea", "price": "₱99", "desc": "Creamy cheesecake series"},
                {"name": "Brown Sugar Boba", "price": "₱89", "desc": "Brown sugar pearls"},
            ],
        },
        {
            "name": "Bubble Tea Station",
            "mapQuery": "Bubble Tea Station Guanzon Kabankalan",
            "rating": "4.4",
            "price": "₱60–₱110",
            "img": "/static/images/bubble-tea-station.jpg",
            "address": "Guanzon St, City Proper",
            "menu": [
                {"name": "Brown Sugar Boba", "price": "₱85", "desc": "Classic brown sugar"},
                {"name": "Taro Milk Tea", "price": "₱80", "desc": "Taro-flavored milk tea"},
            ],
        },
        {
            "name": "Milk Tea ni Juan",
            "mapQuery": "Milk Tea ni Juan Rizal Kabankalan",
            "rating": "4.3",
            "price": "₱50–₱100",
            "img": "/static/images/milk-tea-ni-juan.jpg",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Taro Milk Tea", "price": "₱75", "desc": "Taro-flavored milk tea"},
                {"name": "Okinawa", "price": "₱80", "desc": "Brown sugar milk tea"},
            ],
        },
        {
            "name": "Sugar 'N Ice Milk Tea",
            "mapQuery": "Sugar N Ice Tan Lorenzo Kabankalan",
            "rating": "4.4",
            "price": "₱60–₱130",
            "img": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=800&auto=format&fit=crop",
            "address": "Corner Tan Lorenzo & Sola St., City Proper",
            "menu": [
                {"name": "Classic Milk Tea", "price": "₱75", "desc": "Classic flavor"},
                {"name": "Oat Spanish Latte", "price": "₱120", "desc": "Coffee with oat milk"},
                {"name": "Siomai", "price": "₱50", "desc": "Pair with milk tea"},
            ],
        },
    ],
}

def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def _restaurant_to_dict(restaurant):
    return {
        "name": restaurant.name,
        "mapQuery": restaurant.map_query or restaurant.name,
        "rating": restaurant.rating,
        "price": restaurant.price_range,
        "img": restaurant.img,
        "address": restaurant.address,
        "menu": [
            {"name": m.name, "price": m.price, "desc": m.desc}
            for m in restaurant.menu_items.all()
        ],
    }

CATEGORY_COLORS = {
    "fastfood": ("#e8452c", "#f6a623"),
    "carinderia": ("#2f7d4f", "#9bcf53"),
    "cafe": ("#6b4226", "#c69c6d"),
}

def _placeholder_image(name, category):
    c1, c2 = CATEGORY_COLORS.get(category, ("#555555", "#999999"))
    label = escape((name or "Restaurant")[:28])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
        "</linearGradient></defs>"
        '<rect width="800" height="500" fill="url(#g)"/>'
        '<text x="400" y="250" font-family="Arial, sans-serif" font-size="44" font-weight="bold" '
        f'fill="#ffffff" text-anchor="middle" dominant-baseline="middle">{label}</text>'
        "</svg>"
    )
    return "data:image/svg+xml;charset=utf-8," + quote(svg)

def _resolve_image(item, category):
    img = (item.get("img") or "").strip()
    if img.startswith("http"):
        return img
    if img.startswith("/static/"):
        rel = img[len("/static/"):]
        if finders.find(rel):
            return static(rel)
        return _placeholder_image(item.get("name"), category)
    if img:
        return static(img)
    return _placeholder_image(item.get("name"), category)

def get_food_data():
    data = copy.deepcopy(FOOD_DATA)
    try:
        for r in Restaurant.objects.prefetch_related("menu_items").all():
            cat = (r.category or "carinderia").lower()
            if cat not in data:
                data[cat] = []
            if not any(x["name"] == r.name for x in data[cat]):
                data[cat].append(_restaurant_to_dict(r))
    except Exception:
        pass
    for cat, items in data.items():
        for item in items:
            item["img"] = _resolve_image(item, cat)
            if not item.get("rating"):
                item["rating"] = "4.5"
    return data

TRENDING_NAMES = [
    ("fastfood", "Jollibee (Guanzon)"),
    ("fastfood", "Snackee Restaurant"),
    ("carinderia", "ALONSO's Cansi & Sizzling House"),
    ("carinderia", "Rosalino's Chicken Inasal and Seafood"),
    ("cafe", "Kape Centrale"),
    ("cafe", "Kalamay Artisan Patisserie & Cafe"),
]

def get_trending_data():
    data = get_food_data()
    trending = []
    for category, name in TRENDING_NAMES:
        for item in data.get(category, []):
            if item["name"] == name:
                trending.append(item)
                break
    return trending

# ============================================================
# HOME
# ============================================================
def home(request):
    data = get_food_data()
    reviews = Review.objects.all().order_by("-created_at")
    all_names = []
    for items in data.values():
        for item in items:
            all_names.append(item["name"])
    context = {
        "food_data": json.dumps(data),
        "trending_data": json.dumps(get_trending_data()),
        "reviews": reviews,
        "total_restaurants": len(all_names),
        "verified_names": json.dumps(all_names),
    }
    return render(request, 'index.html', context)

# ============================================================
# ABOUT
# ============================================================
def about(request):
    context = {
        "title": "About Kabankalan Eats",
        "description": "Kabankalan Eats is your dedicated local food guide, exclusively covering the heart of Kabankalan City Proper.",
        "features": [
            {"icon": "🔍", "title": "Discover Local Restaurants", "desc": "Find restaurants in Kabankalan City Proper. From local dishes like Cansi, to fast food, desserts, cafes, and milk tea shops."},
            {"icon": "🍽", "title": "View Menu & Prices", "desc": "See the full menu, prices, and details of each dish right away, so you already know what to order before you even go there."},
            {"icon": "📍", "title": "Map & Location", "desc": "Every restaurant has a complete address and map link, so you can easily find them."},
        ],
    }
    return render(request, "about.html", context)

# ============================================================
# CONTACT
# ============================================================
def contact(request):
    contact_details = {
        "email": "support@kabankalaneats.com",
        "phone": "+63 912 345 6789",
        "address": "Kabankalan City Proper, Negros Occidental",
        "facebook": "https://facebook.com/kabankalaneats",
        "instagram": "https://instagram.com/kabankalaneats",
    }
    return render(request, "contact.html", {"contact_details": contact_details})

# ============================================================
# HELP
# ============================================================
def help_page(request):
    faqs = [
        {"question": "How to search for food?", "answer": "Type what you want in the search bar (e.g. pizza, cansi, milk tea) and press Send.", "link": reverse("food_finder:home") + "#search", "link_text": "Go to Search Bar"},
        {"question": "How to see menu and prices?", "answer": "Click the restaurant card you want. You will see the full menu, prices, address, and map.", "link": reverse("food_finder:home") + "#restaurants", "link_text": "View Restaurants"},
        {"question": "How to go to the restaurant?", "answer": "Inside the menu modal, there is an Open in Maps button. Click it to go directly to 【entity-Google Maps¦canonical_name=Google Maps】.", "link": reverse("food_finder:home") + "#restaurants", "link_text": "Choose a Restaurant"},
        {"question": "How to leave a review?", "answer": "Scroll down on home page, find the System Feedback section. Write your name, pick a rating, and type your comment.", "link": reverse("food_finder:home") + "#feedback", "link_text": "Leave a Review"},
        {"question": "Need more help?", "answer": "If your question is still not answered, contact us.", "link": reverse("food_finder:contact"), "link_text": "Contact Us"},
    ]
    return render(request, "help.html", {"faqs": faqs})

# ============================================================
# AUTH - LOGOUT / LOGIN / REGISTER - FIXED
# ============================================================
def logout_user(request):
    logout(request)
    return redirect('food_finder:home')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("food_finder:home")
        else:
            return render(request, "login.html", {"error": "username or password is incorrect."})
    return render(request, "login.html")

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("food_finder:login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# ============================================================
# SUBMIT REVIEW - FIXED, TUMATANGGAP NG JSON AT FORM
# ============================================================
@require_POST
def submit_review(request):
    # 1. JSON man o Form, kaya basahon
    if "application/json" in (request.content_type or ""):
        try:
            data = json.loads(request.body or b"{}")
        except Exception:
            data = {}
        name = str(data.get("name", "") or "").strip()
        rating = data.get("rating", 5)
        text = str(data.get("text", "") or data.get("comment", "") or data.get("message", "") or "").strip()
    else:
        name = request.POST.get("name", "").strip()
        rating = request.POST.get("rating", "5")
        text = (request.POST.get("text", "") or request.POST.get("comment", "") or request.POST.get("message", "")).strip()

    if not name or not text:
        return JsonResponse({"ok": False, "success": False, "error": "Missing fields - need name and comment"}, status=400)

    # 2. Rating: pwede "5" o "5 (Excellent)" o 5
    try:
        rating_int = int(str(rating).strip().split()[0])
    except (ValueError, TypeError, IndexError):
        rating_int = 5

    if rating_int < 1:
        rating_int = 1
    if rating_int > 5:
        rating_int = 5

    review = Review.objects.create(name=name, rating=rating_int, text=text)
    return JsonResponse({
        "ok": True,
        "success": True,
        "name": review.name,
        "rating": review.rating,
        "stars": review.stars_display,
        "text": review.text,
        "comment": review.text,
        "date": review.created_at.strftime("%B %d, %Y"),
    })