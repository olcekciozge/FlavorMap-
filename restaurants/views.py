from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Category, Review, Favorite, City, ReviewLike, Menu, OpeningHours, RestaurantImage
from django.db.models import Avg, Q, Count, Sum
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

def index(request):
    restaurants = Restaurant.objects.all()

    top_rated = Restaurant.objects.annotate(
        avg_rating=Avg('reviews__rating', filter=Q(reviews__parent__isnull=True))
    ).order_by('-avg_rating')[:5]

    newest = Restaurant.objects.order_by('-id')[:5]

    context = {
        "restaurants": restaurants,
        "top_rated": top_rated,
        "newest": newest
    }

    return render(request, "homepage.html", context)

def restaurant_list(request):

    restaurants = Restaurant.objects.annotate(
        average_rating=Avg("reviews__rating", filter=Q(reviews__parent__isnull=True))
    )

    category = request.GET.get("category")
    price = request.GET.get("price")
    city = request.GET.get("city")
    min_rating = request.GET.get("min_rating")
    sort = request.GET.get("sort")
    query = request.GET.get("q")

    if category:
        restaurants = restaurants.filter(categories_id=category)

    if price:
        restaurants = restaurants.filter(price_range=price)

    if city:
        restaurants = restaurants.filter(city_id=city)

    if min_rating:
        restaurants = restaurants.filter(average_rating__gte=min_rating)

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(city__name__icontains=query) |
            Q(district__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(menus__name__icontains=query)
        ).distinct()


    if sort == "name_asc":
        restaurants = restaurants.order_by("name")
    elif sort == "name_desc":
        restaurants = restaurants.order_by("-name")
    elif sort == "rating_desc":
        restaurants = restaurants.order_by("-average_rating")
    elif sort == "rating_asc":
        restaurants = restaurants.order_by("average_rating")

    return render(request, "allrestaurants.html", {
        "restaurants": restaurants,
        "categories": Category.objects.all(),
        "cities": City.objects.all(),
    })

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
            avg_rating = restaurant.reviews.filter(parent__isnull=True).aggregate(avg=Avg("rating"))["avg"]
            return render(request, "restaurants/restaurantprofile.html", {
                "restaurant": restaurant,
                "reviews": reviews,
                "avg_rating": avg_rating,
                "error_message": "You can't leave it blank!",
            })

        if Review.objects.filter(
                restaurant=restaurant,
                user=request.user,
                parent__isnull=True
        ).exists():
            return redirect("restaurants:detail", id=id)

        try:
            with transaction.atomic():
                Review.objects.create(
                    restaurant=restaurant,
                    user=request.user,
                    text=text,
                    rating=rating
                )
        except IntegrityError:
            reviews = restaurant.reviews.all()
            avg_rating = restaurant.reviews.filter(parent__isnull=True).aggregate(avg=Avg("rating"))["avg"] or 0

            return render(request, "restaurants/restaurantprofile.html", {
                "restaurant": restaurant,
                "reviews": reviews,
                "avg_rating": avg_rating,
                "error_message": "You already reviewed this restaurant!"
            })

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

    reviews = restaurant.reviews.filter(parent__isnull=True).annotate(
        like_count=Count("likes", filter=Q(likes__value=1)),
        dislike_count=Count("likes", filter=Q(likes__value=-1)),
        score=Sum("likes__value")
    ).order_by("-score")

    for r in reviews:
        r.annotated_replies = r.replies.annotate(
            like_count=Count("likes", filter=Q(likes__value=1)),
            dislike_count=Count("likes", filter=Q(likes__value=-1)),
            score=Sum("likes__value")
        ).order_by("-score")

    avg_rating = restaurant.average_rating()

    return render(request, "restaurants/restaurantprofile.html", {
        "restaurant": restaurant,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "is_favorite": is_favorite
    })


def contact(request):
    return render(request, "contact.html", {"title": "Contact Us"})

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


@login_required
def create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        city_id = request.POST.get("city")
        district = request.POST.get("district")
        price_range = request.POST.get("price_range")
        image = request.FILES.get("image")
        images = request.FILES.getlist("images")

        try:
            latitude = float(request.POST.get("latitude")) if request.POST.get("latitude") else None
            longitude = float(request.POST.get("longitude")) if request.POST.get("longitude") else None
        except ValueError:
            latitude = None
            longitude = None

        category_ids = request.POST.getlist("categories")
        menu_ids = request.POST.getlist("menus")
        opening_hour_ids = request.POST.getlist("time")

        if not name or not city_id:
            messages.error(request, "Name and City are required.")
            return redirect("restaurants:create")

        try:
            with transaction.atomic():

                restaurant = Restaurant.objects.create(
                    name=name,
                    description=description,
                    city_id=city_id,
                    district=district,
                    price_range=price_range,
                    image=image,
                    owner=request.user,
                    latitude = latitude,
                    longitude = longitude,
                )

                for img in images:
                    RestaurantImage.objects.create(
                        restaurant=restaurant,
                        image=img
                    )

                if category_ids:
                    restaurant.categories.set(category_ids)

                if menu_ids:
                    restaurant.menus.set(menu_ids)

                if opening_hour_ids:
                    restaurant.time.set(opening_hour_ids)

        except Exception:
            messages.error(request, "Something went wrong while creating restaurant.")
            return redirect("restaurants:create")

        messages.success(request, "Restaurant is successfully added!")
        return redirect("restaurants:index")

    context = {
        "categories": Category.objects.all(),
        "cities": City.objects.all(),
        "menus": Menu.objects.all(),
        "opening_hours": OpeningHours.objects.all(),
    }
    return render(request, "restaurants/addrestaurant.html", context)


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
    reviews = Review.objects.filter(
        user=request.user,
        parent__isnull=True
    )
    owned_restaurants = Restaurant.objects.filter(owner=request.user)

    return render(request, "restaurants/userprofile.html", {
        "favorites": favorites,
        "reviews": reviews,
        "owned_restaurants": owned_restaurants,
    })

@login_required
def add_reply(request, review_id):
    parent_review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            try:
                Review.objects.create(
                    restaurant=parent_review.restaurant,
                    user=request.user,
                    text=text,
                    rating=None,
                    parent=parent_review
                )
            except IntegrityError:
                messages.error(request, "Something went wrong while replying.")

    return redirect("restaurants:detail", id=parent_review.restaurant.id)


@login_required
def toggle_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    value = int(request.POST.get("value"))

    obj, created = ReviewLike.objects.get_or_create(
        user=request.user,
        review=review,
        defaults={"value": value}
    )

    if not created:
        if obj.value == value:
            obj.delete()
        else:
            obj.value = value
            obj.save()

    return redirect("restaurants:detail", id=review.restaurant.id)
@login_required
def edit_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)

    if restaurant.owner != request.user:
        messages.error(request, "You don't have to access to edit restaurant.")
        return redirect("restaurants:profile")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        city_id = request.POST.get("city")
        district = request.POST.get("district")
        price_range = request.POST.get("price_range")

        category_ids = request.POST.getlist("categories")
        menu_ids = request.POST.getlist("menus")
        opening_hour_ids = request.POST.getlist("time")

        if not name or not city_id:
            messages.error(request, "Name and city is required.")
            return redirect("restaurants:edit_restaurant", id=id)

        try:
            with transaction.atomic():

                restaurant.name = name
                restaurant.description = description
                restaurant.city_id = city_id
                restaurant.district = district
                restaurant.price_range = price_range

                if request.FILES.get("image"):
                    restaurant.image = request.FILES.get("image")

                restaurant.save()

                restaurant.categories.set(category_ids)
                restaurant.menus.set(menu_ids)
                restaurant.time.set(opening_hour_ids)

        except Exception:
            messages.error(request, "Something went wrong while editing.")
            return redirect("restaurants:edit_restaurant", id=id)

        messages.success(request, f"{restaurant.name} is successfully edited.")
        return redirect("restaurants:profile")

    context = {
        "restaurant": restaurant,
        "categories": Category.objects.all(),
        "cities": City.objects.all(),
        "menus": Menu.objects.all(),
        "opening_hours": OpeningHours.objects.all(),
    }
    return render(request, "restaurants/edit_restaurant.html", context)


@login_required
def delete_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)

    if restaurant.owner != request.user:
        return redirect('restaurants:profile')

    if request.method == "POST":
        restaurant.delete()
        return redirect("restaurants:profile")

    return render(request, "restaurants/delete_restaurant.html", {"restaurant": restaurant})


@login_required
def add_menu(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        currency = request.POST.get("currency")
        description = request.POST.get("description")
        category = request.POST.get("category")

        if not name or not price:
            messages.error(request, "All fields are required.")
            return redirect("restaurants:add_menu")

        Menu.objects.create(
            name=name,
            description=description,
            price=price,
            currency=currency,
            category=category
        )

        messages.success(request, "Menu added!")
        return redirect("restaurants:create")

    return render(request, "restaurants/add_menu.html")

@login_required
def add_opening_hour(request):
    if request.method == "POST":
        day = request.POST.get("day")
        open_time = request.POST.get("open_time")
        close_time = request.POST.get("close_time")

        OpeningHours.objects.create(
            day=day,
            open_time=open_time,
            close_time=close_time
        )

        return redirect("restaurants:create")

    return render(request, "restaurants/add_opening_hour.html")