import copy
import json
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles import finders
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Restaurant, Review

FOOD_DATA = {
    "fastfood": [
        {
            "name": "Jollibee (Guanzon)",
            "mapQuery": "Jollibee Guanzon St, Kabankalan City",
            "rating": "4.5",
            "price": "₱50–₱250",
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzB9l-kZmFoJPgem5i0XPU5I8cpqvjCZIJpF5W4m4vjrhpQ2OXr7gYJzrc&s=10",
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
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEzC9WY08bwHZYAAmJRWh990g4Ad1HU9-NPnWDcdu--w&s=10",
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
            "img": "https://images.unsplash.com/photo-1513639776629-7b61b0ac49cb?q=80&w=800&auto=format&fit=crop",
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
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZZwhZxixf4-l8MyYxuqSmeIeIPteO6WIN6j9w27CIsQ&s=10",
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
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNTnmxaz3zXgWILSZ_zyfahwpja3N1r8N0qTtIjtx9IQ&s=10",
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
            "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=800&auto=format&fit=crop",
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
            "address": "L1, Gaisano Grand, Tan Lorenzo Street National Road, Corner Barangay 1, Kabankalan City, 6111 Negros Occidental",
            "menu": [
                {"name": "Hawaiian Overload", "price": "₱199", "desc": "Pizza"},
                {"name": "Carbonara", "price": "₱150", "desc": "Creamy pasta"},
                {"name": "Chicken Alfredo", "price": "₱160", "desc": "Pasta with chicken"},
            ],
        },
        {
            "name": "Jollibee (Gaisano)",
            "mapQuery": "Jollibee Gaisano Grand Mall Kabankalan",
            "rating": "4.2",
            "price": "₱30–₱1,575",
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuonu74mrJUGvQFvOgTK_kUhmnybmaHN1wJLdQ7s0v2zdU1NVgM9Ns3F8J&s=10",
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
            "name": "Snackee Restaurant",
            "mapQuery": "Snackee Restaurant South National Road Repollo St Kabankalan City",
            "rating": "4.1",
            "price": "₱1–₱500",
            "img": "https://images.unsplash.com/photo-1562967914-608f82629710?q=80&w=800&auto=format&fit=crop",
            "address": "South National Road, corner Repollo St",
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
    "carinderia": [
        {
            "name": "ALONSO's Cansi & Sizzling House",
            "mapQuery": "Alonsos Cansi Guanzon Kabankalan",
            "rating": "3.9",
            "price": "₱1–₱2,000",
            "img": "https://lh3.googleusercontent.com/gps-cs-s/ANWiy9QOdV1oTuUr8nm9Ao3dWiszHRPZUeMel-uhRIXBLB6jvJEOuYmFhIw3RSwN9YfYbtT4g83d8i2sWOQfjUpfQf25MUkryK_-X6wToOtkRZQ33uHJC9QzHXJhgGbkHtx2WIIt0HF-=w224-h298-n-k-no",
            "address": "Guanzon St, Brgy. 1, Kabankalan City, 6111 Negros Occidental",
            "menu": [
                {"name": "Special Cansi", "price": "₱130", "desc": "Sour beef soup"},
                {"name": "Cansi Bulalo", "price": "₱250", "desc": "Rich beef marrow soup"},
                {"name": "Pork BBQ", "price": "₱100", "desc": "Grilled pork skewers"},
            ],
        },
        {
            "name": "Alma's Ihaw-Ihaw",
            "mapQuery": "Almas Ihaw-Ihaw Rizal St Kabankalan City",
            "rating": "4.9",
            "price": "₱50–₱150",
            "img": "/static/images/almas-ihaw-ihaw.png",
            "address": "Rizal St, City Proper",
            "menu": [
                {"name": "Pork BBQ", "price": "₱100", "desc": "Grilled skewers"},
                {"name": "Chicken BBQ", "price": "₱120", "desc": "Grilled chicken skewers"},
                {"name": "Isaw", "price": "₱30", "desc": "Grilled chicken intestine"},
                {"name": "Puso (Hanging Rice)", "price": "₱15", "desc": "Rice wrapped in coconut leaves"},
            ],
        },
        {
            "name": "Cansi House",
            "mapQuery": "Cansi House Rizal Kabankalan",
            "rating": "4.7",
            "price": "₱120–₱280",
            "img": "",
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
            "img": "",
            "address": "National Highway, Brgy. 1, City Proper",
            "menu": [
                {"name": "Special Cansi", "price": "₱260", "desc": "Sour soup"},
                {"name": "Cansi Regular", "price": "₱180", "desc": "Regular cansi"},
            ],
        },
        {
            "name": "Aida's Chicken - Manokan Country",
            "mapQuery": "Aidas Chicken Manokan Country Kabankalan City",
            "rating": "4.5",
            "price": "₱50–₱100",
            "img": "/static/images/aidas-chicken.png",
            "address": "Public Market, City Proper",
            "menu": [
                {"name": "Adobo with Rice", "price": "₱70", "desc": "Classic adobo"},
                {"name": "Sinigang na Baboy", "price": "₱85", "desc": "Sour pork soup"},
                {"name": "Fried Fish with Rice", "price": "₱75", "desc": "Crispy fried fish"},
            ],
        },
        {
            "name": "Myrna's Restaurant",
            "mapQuery": "Myrnas Restaurant Tan Lorenzo Kabankalan",
            "rating": "4.4",
            "price": "₱80–₱150",
            "img": "/static/images/myrnas-restaurant.png",
            "address": "Tan Lorenzo St, City Proper",
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
            "img": "/static/images/3rd-talabahan.png",
            "address": "Lirazan St, City Proper",
            "menu": [
                {"name": "Baked Talaba", "price": "₱150", "desc": "Fresh oysters"},
                {"name": "Grilled Talaba", "price": "₱120", "desc": "Grilled oysters"},
                {"name": "Kilawin na Talaba", "price": "₱130", "desc": "Fresh oyster ceviche"},
            ],
        },
        {
            "name": "Crispy King",
            "mapQuery": "Crispy King Rizal Street Barangay 9 Kabankalan City",
            "rating": "4.5",
            "price": "₱60–₱120",
            "img": "/static/images/crispy-king.png",
            "address": "XRP8+FV8, Rizal Street, Barangay 9, Kabankalan City, 6111 Negros Occidental",
            "menu": [
                {"name": "Chicken Joy", "price": "—", "desc": "Fried chicken"},
            ],
        },
        {
            "name": "Perico Restaurant",
            "mapQuery": "Perico Restaurant Justice Perez Highway Kabankalan City",
            "rating": "3.9",
            "price": "₱3,000–₱3,500",
            "img": "/static/images/perico-restaurant.png",
            "address": "2R25+4VQ, Justice Perez Highway, Kabankalan City",
            "menu": [],
        },
        {
            "name": "The Melting Pot",
            "mapQuery": "The Melting Pot Rizal Street Kabankalan City",
            "rating": "4.1",
            "price": "",
            "img": "/static/images/melting-pot.png",
            "address": "Rizal Street, Kabankalan City",
            "menu": [],
        },
        {
            "name": "Rosalino's Chicken Inasal and Seafood",
            "mapQuery": "Rosalinos Chicken Inasal and Seafood Sola Street Kabankalan City",
            "rating": "4.5",
            "price": "₱200–₱400",
            "img": "/static/images/rosalinos.png",
            "address": "Sola Street (Plus Code: XRW7+79M), Kabankalan City, Negros Occidental",
            "menu": [
                {"name": "Chicken Inasal", "price": "—", "desc": "Signature charcoal-grilled chicken marinated in lemongrass, garlic, and ginger"},
                {"name": "Sisig", "price": "—", "desc": "Popular sizzling sisig"},
                {"name": "Seafood", "price": "—", "desc": "Assorted seafood dishes"},
                {"name": "Boneless Fried Fish", "price": "—", "desc": "Highly recommended by diners"},
                {"name": "Tacos Salad", "price": "—", "desc": ""},
                {"name": "Coffee Jelly", "price": "—", "desc": "Dessert"},
                {"name": "Leche Flan", "price": "—", "desc": "Dessert"},
                {"name": "Buko Salad", "price": "—", "desc": "Recommended by guests"},
            ],
        },
    ],
    "cafe": [
        {
            "name": "Sol's Garden Cafe",
            "mapQuery": "Sols Garden Cafe Don Emilio Village Phase One Kabankalan",
            "rating": "4.5",
            "price": "₱1–₱500",
            "img": "/static/images/sols-garden-cafe.png",
            "address": "Don Emilio Village Phase One, Brgy. 9, Kabankalan City, 6111 Negros Occidental",
            "menu": [
                {"name": "Sizzling Bangus", "price": "—", "desc": "One of their best-known dishes"},
                {"name": "Garlic Pepper Steak", "price": "—", "desc": "One of their best-known dishes"},
            ],
        },
        {
            "name": "Kalamay Artisan Patisserie & Cafe",
            "mapQuery": "Kalamay Artisan Patisserie & Cafe 42 Lirazan St Kabankalan City",
            "rating": "4.4",
            "price": "₱1–₱500",
            "img": "/static/images/kalamay-cafe.jpg",
            "address": "42 Lirazan St, Barangay 4, Kabankalan City",
            "menu": [],
        },
        {
            "name": "Ayahay Bistro",
            "mapQuery": "Ayahay Bistro Oklahoma Street Kabankalan City",
            "rating": "5.0",
            "price": "",
            "img": "/static/images/ayahay-bistro.png",
            "address": "Oklahoma Street, Brgy 1, Kabankalan City",
            "menu": [
                {"name": "Silog Meals (such as Hotsilog)", "price": "₱59", "desc": "Known for silog meals, such as Hotsilog for ₱59"},
                {"name": "Locally Sourced Dishes", "price": "—", "desc": "Known for locally sourced dishes"},
            ],
        },
        {
            "name": "Kape Centrale",
            "mapQuery": "Kape Centrale Punta Guanzon St Kabankalan City",
            "rating": "",
            "price": "",
            "img": "/static/images/kape-centrale.png",
            "address": "Punta, Guanzon St, Kabankalan City, Negros Occidental",
            "menu": [
                {"name": "Pork Steak", "price": "—", "desc": "Served with rice and corn"},
                {"name": "Tuna Pesto Pasta", "price": "—", "desc": "Pasta with tuna and pesto"},
                {"name": "Carbonara", "price": "—", "desc": "Creamy pasta"},
                {"name": "Caffè Latte", "price": "—", "desc": "Latte coffee"},
                {"name": "Coffee of the Day", "price": "—", "desc": "Brewed coffee"},
                {"name": "Chocolate Cookie Latte", "price": "—", "desc": "Iced chocolate cookie latte"},
                {"name": "Dark Chocolate Milkshake", "price": "—", "desc": "Dark chocolate milkshake with whipped cream"},
                {"name": "Chocolate Cake", "price": "—", "desc": "Dark chocolate cake"},
                {"name": "Choco Cake and Coffee", "price": "—", "desc": "Chocolate cake served with coffee"},
            ],
        },
        {
            "name": "Cafe Mateo",
            "mapQuery": "Cafe Mateo 44 Bonifacio St Kabankalan City",
            "rating": "",
            "price": "",
            "img": "/static/images/cafe-mateo.png",
            "address": "44 Bonifacio St, Kabankalan City, 6111 Negros Occidental",
            "menu": [
                {"name": "Plain Coffee", "price": "₱20", "desc": "Hot drink"},
                {"name": "Café au Lait", "price": "—", "desc": "Hot drink"},
                {"name": "Café Latte", "price": "—", "desc": "Hot drink"},
                {"name": "Bisoffee", "price": "—", "desc": "Hot drink"},
                {"name": "Tablea", "price": "—", "desc": "Hot chocolate drink"},
                {"name": "Bischoco", "price": "—", "desc": "Hot drink"},
                {"name": "Mocha", "price": "—", "desc": "Hot drink"},
                {"name": "Milk", "price": "—", "desc": "Hot drink"},
                {"name": "Sweet Tea", "price": "—", "desc": "Hot tea"},
                {"name": "Herbal Tea", "price": "—", "desc": "Hot tea"},
                {"name": "Budbud", "price": "₱20", "desc": "Food menu item"},
                {"name": "Siopao", "price": "₱30", "desc": "Steamed bun"},
                {"name": "Nacho Fries", "price": "—", "desc": "Food menu item"},
                {"name": "French Fries", "price": "—", "desc": "Food menu item"},
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
    """Offline SVG placeholder (data URI) so a card never shows a broken image."""
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


def _resolve_image(img, name, category):
    """Return a usable image URL; fall back to a placeholder when it can't be shown."""
    img = str(img or "").strip()
    fallback = _placeholder_image(name, category)

    if not img:
        return fallback

    if img.startswith(("http://", "https://", "data:")):
        return img

    # Local static file: make sure it really exists, otherwise use the placeholder.
    static_url = settings.STATIC_URL or "/static/"
    rel = img[len(static_url):] if img.startswith(static_url) else img.lstrip("/")
    if rel.startswith("static/"):
        rel = rel[len("static/"):]
    if finders.find(rel):
        return static(rel)
    return fallback


def _apply_images(data):
    for category, bucket in data.items():
        for entry in bucket:
            entry["fallbackImg"] = _placeholder_image(entry["name"], category)
            entry["img"] = _resolve_image(entry.get("img"), entry["name"], category)


def _build_food_data():
    data = copy.deepcopy(FOOD_DATA)
    trending = []

    for restaurant in Restaurant.objects.prefetch_related("menu_items"):
        entry = _restaurant_to_dict(restaurant)
        bucket = data.setdefault(restaurant.category, [])
        bucket[:] = [r for r in bucket if r["name"] != entry["name"]]
        bucket.append(entry)
        if restaurant.is_trending:
            trending.append(entry)

    _apply_images(data)  # trending entries share these dicts, so they get fixed too

    if not trending:
        everything = [r for bucket in data.values() for r in bucket]
        trending = sorted(everything, key=lambda r: _to_float(r["rating"]), reverse=True)[:6]

    return data, trending


def _json_for_script(value):
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def home(request):
    food_data, trending = _build_food_data()
    names = [r["name"] for bucket in food_data.values() for r in bucket]

    context = {
        "food_data": _json_for_script(food_data),
        "trending_data": _json_for_script(trending),
        "verified_names": _json_for_script(names),
        "total_restaurants": len(names),
        "reviews": Review.objects.all()[:20],
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def help_page(request):
    return render(request, "help.html")


def login_user(request):
    error = ""
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect("food_finder:home")
        error = "Invalid username or password."
    return render(request, "login.html", {"error": error})


def logout_user(request):
    logout(request)
    return redirect("food_finder:home")


@require_POST
def submit_review(request):
    name = request.POST.get("name", "").strip()
    text = request.POST.get("text", "").strip()
    try:
        rating = int(request.POST.get("rating", ""))
    except ValueError:
        rating = 0

    if not name or not text or not 1 <= rating <= 5:
        return JsonResponse({"ok": False, "error": "Invalid review."}, status=400)

    review = Review.objects.create(name=name[:100], rating=rating, text=text)
    return JsonResponse(
        {
            "ok": True,
            "name": escape(review.name),
            "stars": review.stars_display,
            "text": escape(review.text),
            "date": review.created_at.strftime("%B %d, %Y"),
        }
    )

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food_finder:login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# SUBMIT REVIEW - FIXED: isa lang ka #reviewForm
def submit_review(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rating = request.POST.get('rating', '5')
        text = request.POST.get('text', '').strip()
        if name and text:
            try:
                rating_int = int(rating)
            except:
                rating_int = 5
            Review.objects.create(name=name, rating=rating_int, text=text)
            return redirect('/?submitted=1#reviewForm')
    return redirect('/')
