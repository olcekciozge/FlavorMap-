from django.urls import path

from . import views

from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.detail, name="detail"),
    path("category/<int:category_id>/", views.category_restaurants, name="category"),
    path("<int:id>/review/", views.add_review, name="add_review"),
]