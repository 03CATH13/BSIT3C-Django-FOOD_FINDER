import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from apps.food_finder.models import Restaurant, MenuItem
from apps.food_finder.views import FOOD_DATA

print("BEFORE - Restaurant:", Restaurant.objects.count(), "MenuItem:", MenuItem.objects.count())
print("FOOD_DATA keys:", list(FOOD_DATA.keys()) if isinstance(FOOD_DATA, dict) else type(FOOD_DATA))

total_r = 0
total_m = 0
# FOOD_DATA pwede nga dict nga category -> list, ukon list lang
if isinstance(FOOD_DATA, dict):
    items = []
    for cat, lst in FOOD_DATA.items():
        if isinstance(lst, list):
            for r in lst:
                items.append((cat, r))
        elif isinstance(lst, dict):
            items.append((cat, lst))
else:
    items = [("fastfood", r) for r in FOOD_DATA]

for cat, r in items:
    if not isinstance(r, dict):
        continue
    name = r.get("name", "").strip()
    if not name:
        continue
    # category - kon wala sa choices, himuon nga fastfood / carinderia / cafe / desserts / milktea
    category = r.get("category", cat)
    if category not in ["fastfood","carinderia","cafe","desserts","milktea"]:
        # pangitaon base sa ngalan
        low = name.lower()
        if "milk" in low or "tea" in low or "chatime" in low or "coco" in low or "dakasi" in low or "infinitea" in low or "serenitea" in low:
            category = "milktea"
        elif "bakery" in low or "cake" in low or "ribbon" in low or "bibingka" in low or "leche" in low or "halo" in low or "don benito" in low or "sweet" in low or "puto" in low:
            category = "desserts"
        elif "cafe" in low or "coffee" in low or "amore" in low:
            category = "cafe"
        elif "【entity-jollibee¦canonical_name=jollibee】" in low or "mcdonald" in low or "mang inasal" in low or "chowking" in low or "chicken" in low:
            category = "fastfood"
        else:
            category = "carinderia"
    rest, created = Restaurant.objects.get_or_create(
        name=name,
        defaults={
            "category": category,
            "map_query": r.get("mapQuery", r.get("map_query", "")),
            "rating": str(r.get("rating", "0.0")),
            "price_range": r.get("price", r.get("price_range", "")),
            "img": r.get("img", ""),
            "address": r.get("address", ""),
            "is_trending": bool(r.get("is_trending", False)),
        }
    )
    if created:
        total_r += 1
    # Menu
    for m in r.get("menu", []) or []:
        if not isinstance(m, dict):
            continue
        mname = m.get("name", "").strip()
        if not mname:
            continue
        _, mcreated = MenuItem.objects.get_or_create(
            restaurant=rest,
            name=mname,
            defaults={
                "price": str(m.get("price", "")),
                "desc": m.get("desc", ""),
                "img": m.get("img", ""),
            }
        )
        if mcreated:
            total_m += 1

print("NADUGANG - Restaurant:", total_r, "MenuItem:", total_m)
print("AFTER - Restaurant:", Restaurant.objects.count(), "MenuItem:", MenuItem.objects.count())
print("DONE - May unod na ang Admin!")
