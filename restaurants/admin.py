from django.contrib import admin
from .models import Restaurant, Category, Menu, Review, OpeningHours, City
@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('day','open_time', 'close_time')
    search_fields = ('day','open_time', 'close_time')
    fields = ('day','open_time', 'close_time',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name','price',)
    fields = ('name', 'price', 'currency')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    fields = ("name",)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'description')
    list_filter = ('categories', 'city')
    fields = ('name', 'description','owner', 'city', 'district','address', 'categories', 'menus', 'time', 'image','price_range' )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'rating', 'text')
    search_fields = ('restaurant__name',)
    list_filter = ('rating', 'restaurant')