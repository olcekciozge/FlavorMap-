from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Category, Review
from django.db.models import Avg


def index(request):
    restaurants = Restaurant.objects.all()

    context = {
        "restaurants": restaurants
    }
    return render(request, "restaurants/index.html", context)

def category_restaurants(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    restaurants = category.restaurants.all()

    context = {
        "category": category,
        "restaurants": restaurants
    }
    return render(request, "restaurants/category.html", context)

def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)

    try:
        text = request.POST["text"]
        rating = request.POST["rating"]
    except KeyError:
        return render(request, "restaurants/detail.html", {
            "restaurant": restaurant,
            "error_message": "Form eksik!"
        })
    else:
        if text == "" or rating == "":
            return render(request, "restaurants/detail.html", {
                "restaurant": restaurant,
                "error_message": "Boş bırakamazsın!"
            })

        Review.objects.create(
            restaurant=restaurant,
            text=text,
            rating=rating
        )

        return redirect("restaurants:detail", id=id)

def detail(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)

    avg_rating = restaurant.reviews.aggregate(Avg("rating"))

    return render(request, "restaurants/detail.html", {
        "restaurant": restaurant,
        "avg_rating": avg_rating["rating__avg"]
    })