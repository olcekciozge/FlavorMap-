import datetime
from django.test import TestCase
from django.urls import reverse

from .models import Category, Restaurant, Review


def create_category(name="Test Category"):
    return Category.objects.create(name=name)


def create_restaurant(title="Test Restaurant", days=0):
    category = create_category()
    date = datetime.date.today() + datetime.timedelta(days=days)

    return Restaurant.objects.create(
        title=title,
        description="Test desc",
        date=date,
        location="Istanbul",
        capacity=100,
        category=category
    )


class RestaurantModelTests(TestCase):

    def test_ordering(self):
        r1 = create_restaurant("Old", days=-5)
        r2 = create_restaurant("New", days=0)

        restaurants = list(Restaurant.objects.all())

        self.assertEqual(restaurants[0], r2)
        self.assertEqual(restaurants[1], r1)


class IndexViewTests(TestCase):

    def test_no_restaurants(self):
        response = self.client.get(reverse("restaurants:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["restaurants"], [])

    def test_restaurant_listed(self):
        restaurant = create_restaurant()

        response = self.client.get(reverse("restaurants:index"))

        self.assertQuerySetEqual(
            response.context["restaurants"],
            [restaurant]
        )


class DetailViewTests(TestCase):

    def test_detail_view(self):
        restaurant = create_restaurant()

        response = self.client.get(
            reverse("restaurants:detail", args=(restaurant.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["restaurant"], restaurant)

    def test_avg_rating(self):
        restaurant = create_restaurant()

        Review.objects.create(restaurant=restaurant, text="Good", rating=4)
        Review.objects.create(restaurant=restaurant, text="Great", rating=2)

        response = self.client.get(
            reverse("restaurants:detail", args=(restaurant.id,))
        )

        self.assertEqual(response.context["avg_rating"], 3)


class CategoryViewTests(TestCase):

    def test_category_filter(self):
        category1 = create_category("Cat1")
        category2 = create_category("Cat2")

        r1 = Restaurant.objects.create(
            title="R1",
            date=datetime.date.today(),
            location="Istanbul",
            capacity=50,
            category=category1
        )

        Restaurant.objects.create(
            title="R2",
            date=datetime.date.today(),
            location="Istanbul",
            capacity=50,
            category=category2
        )

        response = self.client.get(
            reverse("restaurants:category", args=(category1.id,))
        )

        self.assertQuerySetEqual(
            response.context["restaurants"],
            [r1]
        )


class AddReviewTests(TestCase):

    def test_add_review_success(self):
        restaurant = create_restaurant()

        response = self.client.post(
            reverse("restaurants:add_review", args=(restaurant.id,)),
            {
                "text": "Nice",
                "rating": "5"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(restaurant.reviews.count(), 1)

    def test_add_review_empty(self):
        restaurant = create_restaurant()

        response = self.client.post(
            reverse("restaurants:add_review", args=(restaurant.id,)),
            {
                "text": "",
                "rating": ""
            }
        )

        self.assertContains(response, "Boş bırakamazsın!")

