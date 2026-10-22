from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Restaurant(models.Model):
    """A restaurant listed in the food finder."""
    CUISINE_CHOICES = [
        ('filipino', 'Local & Cansi'),
        ('fast_food', 'Fast Food'),
        ('cafe', 'Cafe & Snacks'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    cuisine_type = models.CharField(max_length=20, choices=CUISINE_CHOICES, default='other')
    contact_number = models.CharField(max_length=20, blank=True)
    opening_hours = models.CharField(max_length=100, blank=True, help_text="e.g., 9:00 AM - 10:00 PM")
    # image = models.ImageField(upload_to='restaurants/', blank=True, null=True)  <-- Naka-comment dahil wala pang Pillow
    
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restaurants_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_restaurant'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.city})"

    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)


class MenuItem(models.Model):
    """A dish or drink offered by a restaurant."""
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_menu_item'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - ₱{self.price} @ {self.restaurant.name}"


class Review(models.Model):
    """A user review of a restaurant."""
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_review'
        ordering = ['-created_at']
        unique_together = ('restaurant', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.restaurant.name} ({self.rating}★)"


class Favorite(models.Model):
    """Bookmarked restaurants by user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_favorite'
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user.username} ♥ {self.restaurant.name}"