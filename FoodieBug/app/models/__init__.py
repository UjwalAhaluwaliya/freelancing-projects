from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Customer') # Customer, RestaurantAdmin, SystemAdmin, DeliveryPartner

    orders = db.relationship('Order', foreign_keys='Order.user_id', backref='customer', lazy=True)
    restaurants = db.relationship('Restaurant', backref='admin', lazy=True) # If role is RestaurantAdmin

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Owner

    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='restaurant', lazy=True)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), default='default_food.jpg')

    customization_groups = db.relationship('CustomizationGroup', backref='menu_item', lazy=True, cascade="all, delete-orphan")

class CustomizationGroup(db.Model):
    __tablename__ = 'customization_groups'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False) # e.g. "Size", "Add-ons"
    type = db.Column(db.String(20), default='single') # 'single' for radio, 'multiple' for checkbox

    options = db.relationship('CustomizationOption', backref='group', lazy=True, cascade="all, delete-orphan")

class CustomizationOption(db.Model):
    __tablename__ = 'customization_options'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('customization_groups.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price_change = db.Column(db.Float, default=0.0)
    icon = db.Column(db.String(50), default='') # Emoji or icon class (e.g., 🧀)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending') # Pending, Preparing, Ready, Out for Delivery, Delivered, PAID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_partner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    delivery_partner = db.relationship('User', foreign_keys=[delivery_partner_id])

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Store snapshot price at time of order
    price_at_order = db.Column(db.Float, nullable=False)

    item = db.relationship('MenuItem')
    customizations = db.relationship('OrderItemCustomization', backref='order_item', lazy=True, cascade="all, delete-orphan")

class OrderItemCustomization(db.Model):
    __tablename__ = 'order_item_customizations'
    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('customization_options.id'), nullable=False)
    
    option = db.relationship('CustomizationOption')

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def get_cart_total(session_cart):
    # This is a helper for calculating cart total from session dict
    total = 0.0
    for item in session_cart:
        total += item['price'] * item['quantity']
    return total
