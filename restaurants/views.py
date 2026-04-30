from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Category, Review, Favorite
from django.db.models import Avg
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
def index(request):
    restaurants = Restaurant.objects.all()

    top_rated = Restaurant.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:5]

    newest = Restaurant.objects.order_by('-id')[:5]

    context = {
        "restaurants": restaurants,
        "top_rated": top_rated,
        "newest": newest
    }

    return render(request, "restaurants/index.html", context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()

    query = request.GET.get("q")
    category = request.GET.get("category")
    city = request.GET.get("city")
    price = request.GET.get("price")

    if query:
        restaurants = restaurants.filter(name__icontains=query)

    if category:
        restaurants = restaurants.filter(categories__id=category)

    if city:
        restaurants = restaurants.filter(city__icontains=city)

    if price:
        restaurants = restaurants.filter(price_range=price)

    categories = Category.objects.all()

    context = {
        "restaurants": restaurants,
        "categories": categories
    }

    return render(request, "restaurants/list.html", context)

def category_restaurants(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    restaurants = category.restaurants.all()

    context = {
        "category": category,
        "restaurants": restaurants
    }
    return render(request, "restaurants/category.html", context)

@login_required
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        rating = request.POST.get("rating")

        if not rating:
            rating = None
        else:
            rating = int(rating)

        if not text or not rating:
            reviews = restaurant.reviews.all()
            avg_rating = reviews.aggregate(Avg("rate_range"))["rating__avg"]
            return render(request, "restaurants/detail.html", {
                "restaurant": restaurant,
                "reviews": reviews,
                "avg_rating": avg_rating,
                "error_message": "You can't leave it blank!",
            })

        if Review.objects.filter(restaurant=restaurant, user=request.user).exists():
            return redirect("restaurants:detail", id=id)

        with transaction.atomic():
            Review.objects.create(
                 restaurant=restaurant,
                 user=request.user,
                 text=text,
                  rating=rating
        )
        return redirect("restaurants:detail", id=id)

    return redirect("restaurants:detail", id=id)

def detail(request,id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            restaurant=restaurant
        ).exists()
    reviews = restaurant.reviews.filter(parent__isnull=True)
    avg_rating = restaurant.reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    return render(request, "restaurants/detail.html", {
        "restaurant": restaurant,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "is_favorite": is_favorite
    })

def about(request):
    return render(request, "restaurants/about.html", {"title": "About FlavorMap"})

def contact(request):
    return render(request, "restaurants/contact.html", {"title": "Contact Us"})

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST.get("confirm")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        return redirect('login')


    return render(request, 'register.html')

def create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        location = request.POST.get("location")

        if name:
            Restaurant.objects.create(
                name=name,
                description=description,
                location=location
            )
            return redirect("restaurants:index")

    return render(request, "restaurants/create.html")

@login_required
def edit_review(request, id):
    review = get_object_or_404(Review, pk=id)

    if review.user != request.user:
        return redirect("restaurants:detail", id=review.restaurant.id)

    if request.method == "POST":
        review.text = request.POST.get("text")
        review.rating = request.POST.get("rating")
        review.save()
        return redirect("restaurants:detail", id=review.restaurant.id)

    return render(request, "restaurants/edit_review.html", {"review": review})

@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, pk=id)

    if review.user != request.user:
        return redirect("restaurants:detail", id=review.restaurant.id)

    if request.method == "POST":
        review.delete()
        return redirect("restaurants:detail", id=review.restaurant.id)

    return render(request, "restaurants/delete_review.html", {"review": review})

@login_required
def toggle_favorite(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)

    fav = Favorite.objects.filter(user=request.user, restaurant=restaurant)

    if fav.exists():
        fav.delete()
    else:
        Favorite.objects.create(user=request.user, restaurant=restaurant)

    return redirect("restaurants:detail", id=id)

def profile(request):
    favorites = Favorite.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    return render(request, "restaurants/profile.html", {
        "favorites": favorites,
        "reviews": reviews
    })

@login_required
def add_reply(request, review_id):
    parent_review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            Review.objects.create(
                restaurant=parent_review.restaurant,
                user=request.user,
                text=text,
                rating=parent_review.rating,
                parent=parent_review
            )

    return redirect("restaurants:detail", id=parent_review.restaurant.id)