from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import current_user, login_required
from app import db
from app.models import User, Restaurant, MenuItem, Order, CustomizationGroup, CustomizationOption
from app.utils.decorators import role_required
import csv
from io import StringIO

admin = Blueprint('admin', __name__)

@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
@role_required('SystemAdmin', 'RestaurantAdmin')
def dashboard():
    if current_user.role == 'SystemAdmin':
        users_count = User.query.count()
        restaurants_count = Restaurant.query.count()
        orders_count = Order.query.count()
        users = User.query.all()
        restaurants = Restaurant.query.all()
        orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        return render_template('admin/dashboard.html', 
                               users_count=users_count, 
                               restaurants_count=restaurants_count, 
                               orders_count=orders_count,
                               users=users,
                               restaurants=restaurants,
                               orders=orders)
    elif current_user.role == 'RestaurantAdmin':
        restaurant = Restaurant.query.filter_by(user_id=current_user.id).first()
        
        if request.method == 'POST' and not restaurant:
            name = request.form.get('restaurant_name')
            location = request.form.get('location')
            contact = request.form.get('contact')
            
            if name and location and contact:
                new_restaurant = Restaurant(name=name, location=location, contact=contact, user_id=current_user.id)
                db.session.add(new_restaurant)
                db.session.commit()
                flash(f"Restaurant '{name}' created successfully!", 'success')
                return redirect(url_for('admin.dashboard'))
                
        if not restaurant:
            return render_template('admin/dashboard.html', restaurant=None)
        orders = Order.query.filter_by(restaurant_id=restaurant.id).order_by(Order.created_at.desc()).all()
        menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
        return render_template('admin/dashboard.html', 
                               restaurant=restaurant, 
                               orders=orders, 
                               menu_items=menu_items)

@admin.route('/manage_menu', methods=['GET', 'POST'])
@login_required
@role_required('RestaurantAdmin')
def manage_menu():
    restaurant = Restaurant.query.filter_by(user_id=current_user.id).first()
    if not restaurant:
        flash("You need a restaurant to manage menu.", "warning")
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_item':
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('base_price')
            
            new_item = MenuItem(
                restaurant_id=restaurant.id,
                name=name,
                description=description,
                base_price=float(price)
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Menu item added successfully!', 'success')
            
        elif action == 'add_customization_group':
            item_id = request.form.get('item_id')
            group_name = request.form.get('group_name')
            group_type = request.form.get('group_type') # 'single' or 'multiple'
            
            new_group = CustomizationGroup(
                item_id=item_id,
                name=group_name,
                type=group_type
            )
            db.session.add(new_group)
            db.session.commit()
            flash('Customization group added!', 'success')
            
        elif action == 'add_customization_option':
            group_id = request.form.get('group_id')
            option_name = request.form.get('option_name')
            price_change = request.form.get('price_change', 0)
            icon = request.form.get('icon', '')
            
            new_option = CustomizationOption(
                group_id=group_id,
                name=option_name,
                price_change=float(price_change),
                icon=icon
            )
            db.session.add(new_option)
            db.session.commit()
            flash('Customization option added!', 'success')
            
        return redirect(url_for('admin.manage_menu'))
        
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('admin/manage_menu.html', menu_items=menu_items)

@admin.route('/download/users')
@login_required
@role_required('SystemAdmin')
def download_users():
    users = User.query.all()
    
    # Generate CSV
    def generate():
        data = StringIO()
        writer = csv.writer(data)
        
        # Header
        writer.writerow(['ID', 'Name', 'Email', 'Role'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
        # Rows
        for user in users:
            writer.writerow([user.id, user.name, user.email, user.role])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=users.csv'})

@admin.route('/download/restaurants')
@login_required
@role_required('SystemAdmin')
def download_restaurants():
    restaurants = Restaurant.query.all()
    
    def generate():
        data = StringIO()
        writer = csv.writer(data)
        
        writer.writerow(['ID', 'Name', 'Location', 'Contact', 'Owner ID'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
        for r in restaurants:
            writer.writerow([r.id, r.name, r.location, r.contact, r.user_id])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=restaurants.csv'})
