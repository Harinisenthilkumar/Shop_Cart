# ShopKart — Django E-Commerce Website

A full-featured fashion e-commerce website built with Python, Django, HTML, CSS and JavaScript.
Inspired by Myntra/Meesho — complete with product listings, cart, wishlist, checkout, orders and user profiles.

---

## Features

- Home page with hero banner, categories, featured/trending/new products
- Product listing with filters (category, price range) and sorting
- Product detail page with size selector, add to cart, wishlist, reviews
- Shopping cart with quantity controls
- Checkout with address and payment method selection
- Order history and order tracking
- Wishlist (login required)
- User profile dashboard
- User registration and login
- Admin panel to manage products, orders, categories
- Fully responsive design (mobile, tablet, desktop)
- Toast notifications for cart/wishlist actions

---

## Tech Stack

- **Backend**: Python 3.11, Django 5
- **Database**: SQLite (dev) — swap to PostgreSQL for production
- **Frontend**: Django Templates, Vanilla JS, Custom CSS
- **Fonts**: Playfair Display + DM Sans (Google Fonts)
- **Images**: Unsplash (demo product images)

---

## Setup Instructions

### 1. Clone / unzip the project

```bash
cd shopkart
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Seed demo data (categories + 20+ products)

```bash
python manage.py seed_data
```

### 6. Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Open in browser

```
http://127.0.0.1:8000/        ← Main website
http://127.0.0.1:8000/admin/  ← Admin panel
```

---

## Project Structure

```
shopkart/
├── shopkart/           ← Django project config
│   ├── settings.py
│   └── urls.py
├── store/              ← Main app
│   ├── models.py       ← Category, Product, Cart, Order, Wishlist, Review
│   ├── views.py        ← All views
│   ├── urls.py         ← URL routing
│   ├── admin.py
│   ├── context_processors.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py   ← Demo data seeder
│   ├── templates/store/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── product_card.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_success.html
│   │   ├── my_orders.html
│   │   ├── wishlist.html
│   │   ├── profile.html
│   │   ├── login.html
│   │   └── register.html
│   └── static/store/
│       ├── css/style.css
│       └── js/main.js
├── manage.py
└── requirements.txt

