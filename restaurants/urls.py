from django.urls import path

from . import views

from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path("", views.index, name="index"),
    path("restaurants/", views.restaurant_list, name="list"),
    path("restaurants/<int:id>/", views.detail, name="detail"),
    path("restaurants/<int:id>/review/", views.add_review, name="add_review"),
    path("category/<int:category_id>/", views.category_restaurants, name="category"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]