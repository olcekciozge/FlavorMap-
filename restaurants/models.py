from django.db import models
from django.db.models import Avg

class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="restaurants")
    menus = models.ManyToManyField(Menu, related_name="restaurant_menus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PRICE_CHOICES = [
        (1, '€'),
        (2, '€€'),
        (3, '€€€'),
    ]
    price_range = models.IntegerField(choices=PRICE_CHOICES, blank=True, default=1)

    # ÖNEMLİ: Hata buradaydı, 'rate_range' yerine 'rating' olmalı
    def average_rating(self):
        avg = self.reviews.aggregate(Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else 0

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    RATE_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐')
    ]
    rating = models.IntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}"