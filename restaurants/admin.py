from django.contrib import admin
from .models import Restaurant, Category, MenuCategory, MenuItem, Review

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name','price')

admin.site.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)