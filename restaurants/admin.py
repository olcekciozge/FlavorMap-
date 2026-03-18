from django.contrib import admin
from .models import Restaurant, Category

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)