from django.db import models

class Restaurant(models.Model):
    CATEGORY_CHOICES = [
        ('fastfood', 'Fast Food'),
        ('carinderia', 'Local & Cansi'),
        ('cafe', 'Cafe & Snacks'),
        ('desserts', 'Desserts'),
        ('milktea', 'Milk Tea'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    map_query = models.CharField(max_length=300, blank=True)
    rating = models.CharField(max_length=10, default='0.0')
    price_range = models.CharField(max_length=50, blank=True)
    img = models.URLField(max_length=500, blank=True)
    address = models.CharField(max_length=300, blank=True)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    desc = models.CharField(max_length=300, blank=True)
    img = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def stars_display(self):
        return '⭐' * self.rating

    def __str__(self):
        return f"{self.name} ({self.rating}★)"