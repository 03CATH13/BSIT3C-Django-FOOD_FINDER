from django.contrib import admin
from .models import Restaurant, MenuItem, Review

admin.site.site_header = "FOOD FINDER Admin"
admin.site.site_title = "Food Finder"
admin.site.index_title = "Welcome to Food Finder Admin"

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'price', 'desc', 'img')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'rating', 'price_range', 'address', 'is_trending')
    list_filter = ('category', 'is_trending')
    search_fields = ('name', 'address')
    list_editable = ('is_trending', 'rating')
    inlines = [MenuItemInline]
    fieldsets = (
        ('Restaurant Info', {
            'fields': ('name', 'category', 'address', 'map_query')
        }),
        ('Details', {
            'fields': ('rating', 'price_range', 'img', 'is_trending')
        }),
    )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant', 'price', 'desc')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')
    fieldsets = (
        (None, {
            'fields': ('restaurant', 'name', 'price', 'desc', 'img')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'stars_display', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'text')
    readonly_fields = ('created_at', 'stars_display')
    fieldsets = (
        (None, {
            'fields': ('name', 'rating', 'text', 'stars_display', 'created_at')
        }),
    )