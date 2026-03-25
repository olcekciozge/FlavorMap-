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
    categories = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="restaurants")
    menus = models.ManyToManyField(Menu,related_name="menus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PRICE_CHOICES = [
        (1, '€'),
        (2, '€€'),
        (3, '€€€'),
    ]

    price_range = models.IntegerField(choices=PRICE_CHOICES, blank=True)

    def average_rating(self):
        return self.reviews.aggregate(Avg("rate_range"))["rate_range__avg"]

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    RATE_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4,'⭐⭐⭐⭐' ),
        (5, '⭐⭐⭐⭐⭐')
    ]

    rating = models.IntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}"
