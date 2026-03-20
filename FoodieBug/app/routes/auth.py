from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'Customer') # Default to Customer

        # Form validation
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered! Please login.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            if not next_page:
                if user.role == 'SystemAdmin':
                    next_page = url_for('admin.dashboard')
                elif user.role == 'RestaurantAdmin':
                    next_page = url_for('admin.dashboard')
                elif user.role == 'DeliveryPartner':
                    next_page = url_for('delivery.dashboard')
                else:
                    next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
