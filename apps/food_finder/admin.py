from django.contrib import admin
from .models import Restaurant, MenuItem, Review, Favorite


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'city', 'average_rating', 'created_at')
    list_filter = ('cuisine_type', 'city')
    search_fields = ('name', 'city', 'address')
    inlines = [MenuItemInline, ReviewInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_vegetarian', 'is_available')
    list_filter = ('is_vegetarian', 'is_available')
    search_fields = ('name', 'restaurant__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'restaurant__name', 'comment')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'added_at')
    search_fields = ('user__username', 'restaurant__name')