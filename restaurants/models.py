from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=50)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='restaurants',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.restaurant.title} - {self.rating}"
