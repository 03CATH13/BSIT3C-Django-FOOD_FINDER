from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Restaurant,
    MenuItem,
    Review,
    Favorite,
    UserProfile,
)


# ============================================
# INLINE ADMINS
# ============================================

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'price', 'is_vegetarian', 'is_available')


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('user', 'rating', 'comment', 'created_at')
    readonly_fields = ('created_at',)


# ============================================
# RESTAURANT ADMIN
# ============================================

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'cuisine_type',
        'contact_number',
        'average_rating',
        'review_count',
        'added_by',
        'created_at',
    )
    list_filter = ('cuisine_type', 'city', 'created_at')
    search_fields = ('name', 'address', 'city', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MenuItemInline, ReviewInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'cuisine_type')
        }),
        ('Location & Contact', {
            'fields': ('address', 'city', 'contact_number', 'opening_hours')
        }),
        ('Metadata', {
            'fields': ('added_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def average_rating(self, obj):
        return f"⭐ {obj.average_rating()}"
    average_rating.short_description = 'Avg Rating'

    def review_count(self, obj):
        return obj.review_count()
    review_count.short_description = 'Reviews'


# ============================================
# MENU ITEM ADMIN
# ============================================

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'restaurant',
        'price',
        'is_vegetarian',
        'is_available',
        'created_at',
    )
    list_filter = ('is_vegetarian', 'is_available', 'restaurant')
    search_fields = ('name', 'description', 'restaurant__name')
    ordering = ('restaurant', 'name')
    readonly_fields = ('created_at',)
    list_editable = ('is_available', 'is_vegetarian')


# ============================================
# REVIEW ADMIN
# ============================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'restaurant',
        'user',
        'rating',
        'short_comment',
        'created_at',
    )
    list_filter = ('rating', 'created_at', 'restaurant')
    search_fields = ('user__username', 'restaurant__name', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def short_comment(self, obj):
        if obj.comment:
            return obj.comment[:50] + ('...' if len(obj.comment) > 50 else '')
        return '—'
    short_comment.short_description = 'Comment'


# ============================================
# FAVORITE ADMIN
# ============================================

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'added_at')
    list_filter = ('added_at', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')
    ordering = ('-added_at',)
    readonly_fields = ('added_at',)


# ============================================
# USER PROFILE INLINE (sa User Admin)
# ============================================

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('age', 'address', 'phone_number')


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'date_joined',
    )


# I-unregister ang default User admin at i-register ang custom
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ============================================
# ADMIN SITE HEADER
# ============================================

admin.site.site_header = "KabankalanEats Admin"
admin.site.site_title = "KabankalanEats Admin Portal"
admin.site.index_title = "Welcome to the Food Finder Management System"