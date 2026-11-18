from django.contrib import admin
from django.apps import apps
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating_stars', 'short_text', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'text')
    ordering = ()
    list_per_page = 20
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Feedback', {'fields': ('name', 'rating', 'text')}),
        ('Info', {'fields': ('created_at',)}),
    )
    def short_text(self, obj):
        text = obj.text or ''
        if len(text) > 50:
            return text[:50] + '...'
        return text
    def rating_stars(self, obj):
        try:
            r = int(obj.rating or 0)
        except:
            r = 0
        return '★' * r + '☆' * (5 - r)
    rating_stars.short_description = 'Rating'
    short_text.short_description = 'Comment'

try:
    from .models import MenuItem
    @admin.register(MenuItem)
    class MenuItemAdmin(admin.ModelAdmin):
        list_display = ('name', 'restaurant', 'price')
        list_filter = ('restaurant',)
        search_fields = ('name', 'restaurant__name')
        list_per_page = 100
        ordering = ()
except Exception:
    pass

try:
    from .models import Restaurant
    @admin.register(Restaurant)
    class RestaurantAdmin(admin.ModelAdmin):
        list_display = ('name', 'address_with_space', 'category', 'rating', 'is_trending')
        list_filter = ('category', 'is_trending')
        search_fields = ('name', 'address')
        list_per_page = 100
        ordering = ()
        def address_with_space(self, obj):
            a = (obj.address or '').replace(',', ', ').replace('  ', ' ').strip()
            return a
        address_with_space.short_description = 'Address'
except Exception:
    pass

for _m in apps.get_app_config('food_finder').get_models():
    if _m.__name__ in ('Review', 'MenuItem', 'Restaurant'):
        continue
    try:
        admin.site.register(_m)
    except Exception:
        pass
