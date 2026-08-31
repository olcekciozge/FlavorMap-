# FlavorMap

FlavorMap is a Django-based web application that allows users to discover, review, and manage restaurants. Users can explore restaurants, filter them based on preferences, leave reviews, and save their favorite places.

---

##  Features

###  User Features

* User registration and authentication
* Write, edit, and delete reviews
* Reply to other users reviews
* Like / dislike reviews
* Add restaurants to favorites
* Personal profile page:

  * Favorite restaurants
  * User reviews
  * Owned restaurants

###  Restaurant Features

* Browse all restaurants
* Filter by:

  * Category
  * City
  * Price range
  * Minimum rating
* Search by name, description, category, or menu
* Sort results (name, rating)

###  Review System

* One main review per user per restaurant
* Nested replies (threaded discussions)
* Like / dislike system for reviews
* Average rating calculation

###  Restaurant Management

* Authenticated users can:

  * Add new restaurants
  * Upload main image + gallery images
  * Add menus
  * Define opening hours
  * Edit or delete their own restaurants

###  Extra Features

* Google Maps integration (via latitude & longitude)
* Image gallery with lightbox
* Dynamic menu display
* Opening hours display

---

##  Project Structure

```
FlavorMap/
│
├── config/                # Django project settings
├── restaurants/          # Main app
│   ├── migrations/
│   ├── templates/        # Detail templates
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/            # Global templates
│   ├── homepage.html
│   ├── allrestaurants.html
│   ├── contact.html
│   ├── login.html
│   ├── register.html
│   └── main.html
│
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

##  Models Overview

* **Restaurant**: Core entity with location, categories, menus, and images
* **Category**: Restaurant categories (e.g., Cafe, Fast Food)
* **City**: Location grouping
* **Menu**: Food items with pricing and currency
* **OpeningHours**: Weekly schedule
* **Review**: User reviews with ratings and replies
* **Favorite**: User’s saved restaurants
* **ReviewLike**: Like/dislike system
* **RestaurantImage**: Additional gallery images

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/olcekciozge/FlavorMap
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
python -m pip install Pillow
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create superuser

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

---

##  Authentication

* Uses Django’s built-in authentication system
* Login & registration pages included
* Access control with `@login_required`

---

##  Admin Panel

Access the admin panel at:

```
http://127.0.0.1:8000/admin/
```

Manage:

* Restaurants
* Categories
* Menus
* Reviews
* Opening Hours
* Cities

---

##  Technologies Used

* Python 3.14
* Django 5.2
* SQLite (default database)
* HTML5 / CSS3
* JavaScript

---

##  Author

Developed by **Megabite Team**

*   Özge Ölçekçi
*   Rümeysa Erdoğan
*   Batuhan Akkol

---


##  License

This project is for educational purposes.
