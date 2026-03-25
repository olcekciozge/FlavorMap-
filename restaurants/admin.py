from django.contrib import admin
from .models import Restaurant, Category, Menu, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'city', 'price_range')
    search_fields = ('name', 'description', 'city')
    list_filter = ('categories', 'city') # 'category' yerine 'categories'

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'rating', 'text')
    search_fields = ('text',)
    list_filter = ('rating', 'restaurant')