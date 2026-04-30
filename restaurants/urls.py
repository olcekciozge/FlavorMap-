from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "restaurants"

urlpatterns = [
    path("", views.index, name="index"),
    path("restaurants/", views.restaurant_list, name="list"),
    path("restaurants/<int:id>/", views.detail, name="detail"),
    path("restaurants/<int:id>/review/", views.add_review, name="add_review"),
    path('review/edit/<int:id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:id>/', views.delete_review, name='delete_review'),
    path("category/<int:category_id>/", views.category_restaurants, name="category"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('register/', views.register, name='register'),
    path('create/', views.create, name='create'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('favorite/<int:id>/', views.toggle_favorite, name='favorite'),
    path('profile/', views.profile, name='profile'),
    path('reply/<int:review_id>/', views.add_reply, name='add_reply'),

]