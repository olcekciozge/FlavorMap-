from django.db import models
from django.db.models import Avg, Q
from django.contrib.auth.models import User

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

class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="restaurants")
    menus = models.ManyToManyField(Menu, related_name="restaurant_menus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    PRICE_CHOICES = [
        (1, '€'),
        (2, '€€'),
        (3, '€€€'),
    ]
    price_range = models.IntegerField(choices=PRICE_CHOICES, blank=True, default=1)

    def average_rating(self):
        avg = self.reviews.filter(parent__isnull=True).aggregate(Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else 0
    def __str__(self):
        return self.name

class OpeningHours(models.Model):
    DAY_CHOICES = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    ]

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="hours"
    )

    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.get_day_display()}: {self.open_time} - {self.close_time}"

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    RATE_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐')
    ]
    rating = models.IntegerField(choices=RATE_CHOICES, null=True, blank=True)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'user'],
                condition=Q(parent__isnull=True),
                name='unique_main_review'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}  ({self.rating})"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'restaurant')


class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'review')

