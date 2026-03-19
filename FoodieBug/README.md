# 🍔 FoodieBug – Online Food Delivery Web Application

FoodieBug is a full-stack web-based food delivery platform built using Flask and MySQL. It enables customers to order customized food, restaurants to manage orders, and delivery partners to handle real-time deliveries with map tracking.

---

## 🔧 Tech Stack

* **Backend:** Python (Flask)
* **Database:** MySQL (Flask-SQLAlchemy, PyMySQL)
* **Authentication:** Flask-Login, Flask-Bcrypt
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6)
* **UI Framework:** Bootstrap 5
* **Maps & Tracking:** Leaflet.js (OpenStreetMap)

---

## 🎯 Key Features

### 👤 Multi-Role System

* **Customer:** Browse menus, customize food, place orders, track history
* **Restaurant Admin:** Manage menu, customization options, view incoming orders
* **Delivery Partner:** Accept and deliver orders via dedicated dashboard
* **System Admin:** View analytics and download system data (CSV)

---

### 🍔 Food Customization Engine

* Dynamic customization with:

  * Add-ons (e.g., Extra Cheese, Jalapeños)
  * Remove ingredients
  * Single-select & multi-select options
* Real-time price updates
* Backend auto-handles dynamic customization mapping in database

---

### 🛒 Smart Cart System

* Session-based cart
* Prevents ordering from multiple restaurants simultaneously
* AJAX-based seamless interaction

---

### 📦 Order & Delivery System

* Complete order lifecycle:

  * Pending → Preparing → Out for Delivery → Delivered
* Delivery partner assignment with order locking
* Each order linked with a specific delivery partner

---

### 🗺️ Live Delivery Tracking

* Integrated **Leaflet.js map**
* Displays:

  * Restaurant location
  * Customer location
  * Delivery route
* Dynamic route generation using order-based coordinates

---

### 💳 Payment System (Demo)

* Simulated payment flow
* Orders marked as "PAID" without real gateway integration

---

### 📊 Admin Dashboard

* System-wide analytics
* CSV export features:

  * Users data
  * Restaurants data

---

### 💡 Additional Features

* Indian currency support (₹)
* Clean, minimal UI with animations
* Dynamic modal-based customization
* Secure authentication & role-based access

---

## ⚙️ Setup Instructions

1. Clone the repository

2. Configure MySQL database:
   mysql+pymysql://root:2202@localhost/foodiebug

3. Initialize database:
   flask --app run init-db

4. Run the application:
   flask run

---

## 🔐 Demo Accounts

* Admin: [admin@foodiebug.com](mailto:admin@foodiebug.com)
* Restaurant: [bk@foodiebug.com](mailto:bk@foodiebug.com)
* Customer: [john@example.com](mailto:john@example.com)

---

## 🚀 Project Goal

To build a scalable, customizable, and real-time food delivery system with advanced features like dynamic food customization, delivery tracking, and multi-role management.

---

## 📌 Future Enhancements

* Real-time tracking with live GPS
* Payment gateway integration
* Mobile app support
* AI-based food recommendations

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
In depth:
# FoodieBug - Online Food Delivery Web Application 🍔

A complete, modern online food delivery platform built with Python (Flask), MySQL, and Bootstrap 5. It features robust user authentication, restaurant menu management, an advanced food customization system, a dynamic cart, and role-based admin panels.

---

## 🏗️ Core Architecture & Technical Flow

**1. User System & Roles (`app/routes/auth.py` & `admin.py`)**
* Fully working User Registration and Authentication using `Flask-Login` and `Flask-Bcrypt`.
* Three primary roles implemented securely using a custom `@role_required` decorator middleware:
  * **Customer:** Can browse menus, add items to cart, and track order histories.
  * **RestaurantAdmin:** Can self-register a Restaurant entity via their Dashboard immediately after signing up, manage their specific Menu Items, set up Customization options (Single/Multiple), and view live Orders placed at their restaurant.
  * **DeliveryPartner:** Dedicated role for delivery riders. Features a unique dashboard pulling globally "Ready" orders. Upon accepting an order, they receive an immersive, Leaflet-powered live mapping simulation routing from the Restaurant to the Customer. 
  * **SystemAdmin:** Has global oversight. Can view total stats on the dashboard and dynamically download CSV backups of the `Users` and `Restaurants` tables directly streamed from the database.

**2. Database Relational Schema (`app/models/__init__.py`)**
* Built with Flask-SQLAlchemy (ORM) using the `PyMySQL` driver.
* Robust relational bindings setup representing: `User`, `Restaurant` (One-to-Many with User), `MenuItem` (One-to-Many with Restaurant), `CustomizationGroup`, `CustomizationOption`, `Order` (Tracks status: Pending, PAID, Preparing, Delivered. Safely stores `delivery_partner_id` to strictly lock orders to a single accepted rider), `OrderItem`, `OrderItemCustomization`, and `Payment`.

**3. Dynamic Cart & Customization Engine (`app/routes/main.py` & `app/static/js/main.js`)**
* **Hardcoded Universal Toppings:** A permanent "Extra Toppings" customization group (Extra Cheese +₹20, Jalapeños +₹15, Extra Sauce +₹10) is injected dynamically into the JSON API response (`/api/menu_item/<id>`) of *every* menu item. Customers will always see these options even if the restaurant forgot to add customizations.
* **On-the-Fly Database Instantiation:** When a customer checks out with these "dummy/default" global toppings, the backend automatically intercepts them, creates genuine database option records under that specific Restaurant's menu item on the fly, and securely links the foreign keys. This prevents database Foreign Key crashes and ensures the Restaurant Owner sees the exact toppings ordered on their dashboard.
* **Aggressive Cart Lock-In:** Implemented strict anti-mixing logic in the `add_to_cart` endpoint. A user is rejected with a JSON Alert Error if they attempt to place foods from *multiple different restaurants* into the same session cart simultaneously, enforcing standard 1-Restaurant-Per-Order rules (like UberEats or Zomato).

**4. UI, Map & Aesthetics (`app/templates` & `app/static/css/style.css`)**
* Designed with clean typography (Google Fonts _Outfit_), Emoji art, and a minimalist text-focused layout.
* Modern interface with floating hover animations (`transform: translateY`), pill-shaped buttons, and `shadow-sm` borders.
* Built dynamic Javascript Modals for the customer ordering flow where checkboxes/radios instantly update a live price tracker before submitting via AJAX `fetch()`.
* **Live Route Tracking Map:** Embedded a brilliant, free OpenStreetMap + Leaflet.js simulated mapping routing box that algorithmically sets coordinates based on Order IDs and accurately renders Pick-up, Drop-off, and Driver locations with dotted routing lines.
* **Currency Localization:** Native Indian Rupees (`₹`) string formatting (`%.2f`) completely replaces Dollars (`$`) across the entire Python backend and all Javascript/Jinja HTML interfaces.

---

## 🛠️ Technology Stack

- **Backend:** Python + Flask
- **Database:** MySQL + Flask-SQLAlchemy (ORM) + PyMySQL
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6), Bootstrap 5

---

## ⚙️ Setup and Installation

### 1. Requirements

Make sure you have **Python 3.8+** and **MySQL Server** installed and running on your device.

### 2. Environment Setup

Create a virtual environment (optional but recommended) and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
```

### 3. Database Configuration

By default, the application is configured to connect to a local MySQL database with the user `root` and password `2202`. 
Ensure your MySQL server is running, and create the database named `foodiebug`:

```sql
CREATE DATABASE foodiebug;
```

*(You can also modify the `SQLALCHEMY_DATABASE_URI` in `config.py` if your database credentials differ.)*

### 4. Initialize Database & Seed Sample Data

Run the CLI command to automatically generate the required database tables and insert sample demo data (restaurants, menu items, customizations, and admin accounts):

```bash
flask --app run init-db
```

### 5. Run the Application

Start the Flask development server:

```bash
python run.py
```

The app will be available at: **http://127.0.0.1:5000**

---

## 🔐 Demo Accounts

The database seeding command (`init-db`) automatically creates these three accounts for testing:

1. **System Admin**
   - **Email:** `admin@foodiebug.com` 
   - **Password:** `admin123` 

2. **Restaurant Admin (Burger King)**
   - **Email:** `bk@foodiebug.com`
   - **Password:** `rest123`

3. **Customer**
   - **Email:** `john@example.com`
   - **Password:** `cust123`

*(You can freely register new accounts directly from the UI and select "Delivery Partner" to view the mapping demo!)*

---

## 📁 Project Structure

```
FoodieBug/
│
├── app/
│   ├── __init__.py           # Application Factory & Blueprints Registration
│   ├── models/
│   │   └── __init__.py       # SQLAlchemy Relational Models 
│   ├── routes/
│   │   ├── admin.py          # Dashboard, CSV exports, Restaurant Creation & Menu controls
│   │   ├── auth.py           # Registration & login flows
│   │   ├── customer.py       # Order history & profile tracking
│   │   ├── delivery.py       # Live Delivery Dashboard, routing algorithms & status controllers
│   │   └── main.py           # Public storefront, menus & strict JSON Cart APIs
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Bespoke UI/styles (colors, animations, sizing)
│   │   └── js/
│   │       └── main.js       # Dynamic AJAX modal and custom cart logic
│   ├── templates/            # Jinja2 HTML Templates
│   │   ├── base.html
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── customer/
│   │   ├── delivery/         # Contains Leaflet mapping UI & Live tracker Dashboard
│   │   └── main/
│   └── utils/
│       ├── decorators.py     # Role-based middleware (@role_required)
│       └── seed.py           # Start point configurations & logic
│
├── config.py                 # Core Configuration Keys / URI pointing to MySQL root:2202
├── requirements.txt          # PIP dependencies
└── run.py                    # Entry script
```

---

Enjoy using the FoodieBug platform!


---

🔥 Developed as a full-stack freelance-ready project with production-level architecture and modern UI/UX.
