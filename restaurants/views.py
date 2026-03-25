from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Category, Review
from django.db.models import Avg


def index(request):
    restaurants = Restaurant.objects.all()
    context = {"restaurants": restaurants}
    return render(request, "restaurants/index.html", context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    context = {"restaurants": restaurants}
    return render(request, "restaurants/list.html", context)

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

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        rating = request.POST.get("rating", "").strip()

        if not text or not rating:
            reviews = restaurant.reviews.all()
            avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
            return render(request, "restaurants/detail.html", {
                "restaurant": restaurant,
                "reviews": reviews,
                "avg_rating": avg_rating,
                "error_message": "You can't leave it blank!",
            })

        Review.objects.create(
            restaurant=restaurant,
            text=text,
            rating=rating
        )
        return redirect("restaurants:detail", id=id)

    return redirect("restaurants:detail", id=id)

def detail(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    reviews = restaurant.reviews.all()
    avg_rating = restaurant.reviews.aggregate(Avg("rating"))["rating__avg"]

    return render(request, "restaurants/detail.html", {
        "restaurant": restaurant,
        "reviews": reviews,
        "avg_rating": avg_rating["rating__avg"]
    })

def about(request):
    return render(request, "restaurants/about.html", {"title": "About FlavorMap"})

def contact(request):
    return render(request, "restaurants/contact.html", {"title": "Contact Us"})