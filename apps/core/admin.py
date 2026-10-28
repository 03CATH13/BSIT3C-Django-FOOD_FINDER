from django.contrib import admin
from .models import Order


# ============================================
# ORDER ADMIN
# ============================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant_name', 'items', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'restaurant_name', 'items')
    list_editable = ('status',)  # Pwede nimo usbon ang status direkta sa listahan
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)