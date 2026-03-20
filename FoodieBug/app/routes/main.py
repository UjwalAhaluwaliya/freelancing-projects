from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.models import Restaurant, MenuItem, CustomizationGroup, CustomizationOption, Order, OrderItem, OrderItemCustomization, Payment
from app import db
from flask_login import current_user, login_required
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    restaurants = Restaurant.query.all()
    return render_template('main/index.html', restaurants=restaurants)

@main.route('/restaurant/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('main/menu.html', restaurant=restaurant, menu_items=menu_items)

@main.route('/api/menu_item/<int:item_id>')
def api_get_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    groups = CustomizationGroup.query.filter_by(item_id=item.id).all()
    
    customizations = []
    for group in groups:
        options = []
        for opt in group.options:
            options.append({
                'id': opt.id,
                'name': opt.name,
                'price_change': opt.price_change,
                'icon': opt.icon
            })
        customizations.append({
            'id': group.id,
            'name': group.name,
            'type': group.type,
            'options': options
        })
        
    customizations.append({
        'id': 'd_grp',
        'name': 'Extra Toppings (Default)',
        'type': 'multiple',
        'options': [
            {'id': 'd_opt1', 'name': 'Extra Cheese', 'price_change': 20.0, 'icon': '🧀'},
            {'id': 'd_opt2', 'name': 'Spicy Jalapeños', 'price_change': 15.0, 'icon': '🌶️'},
            {'id': 'd_opt3', 'name': 'Extra Sauce', 'price_change': 10.0, 'icon': '🥫'},
        ]
    })
        
    return jsonify({
        'id': item.id,
        'name': item.name,
        'base_price': item.base_price,
        'description': item.description,
        'customizations': customizations
    })

@main.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', [])
    total = sum([(i['base_price'] + sum([opt['price_change'] for opt in i['customizations']])) * i['quantity'] for i in cart])
    return render_template('main/cart.html', cart=cart, total=total)

@main.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []
        
    data = request.json
    item_id = data.get('item_id')
    quantity = int(data.get('quantity', 1))
    selected_options = data.get('options', []) # ids of options
    
    item = MenuItem.query.get_or_404(item_id)
    
    if session['cart']:
        if session['cart'][0]['restaurant_id'] != item.restaurant_id:
            return jsonify({'status': 'error', 'message': 'You can only order from ONE restaurant at a time. Please clear your cart first to order from here.'}), 400
            
    customizations = []
    
    dummy_map = {
        'd_opt1': {'name': 'Extra Cheese', 'price_change': 20.0, 'icon': '🧀'},
        'd_opt2': {'name': 'Spicy Jalapeños', 'price_change': 15.0, 'icon': '🌶️'},
        'd_opt3': {'name': 'Extra Sauce', 'price_change': 10.0, 'icon': '🥫'},
    }
    
    for opt_id in selected_options:
        opt_id_str = str(opt_id)
        if opt_id_str in dummy_map:
            dummy = dummy_map[opt_id_str]
            customizations.append({
                'id': opt_id_str,
                'name': dummy['name'],
                'price_change': dummy['price_change'],
                'icon': dummy['icon']
            })
        else:
            opt = CustomizationOption.query.get(opt_id)
            if opt:
                customizations.append({
                    'id': opt.id,
                    'name': opt.name,
                    'price_change': opt.price_change,
                    'icon': opt.icon
                })
            
    # Add item to session cart
    cart_item = {
        'id': len(session['cart']), # dummy unique id for cart
        'item_id': item.id,
        'name': item.name,
        'base_price': item.base_price,
        'restaurant_id': item.restaurant_id,
        'restaurant_name': item.restaurant.name,
        'quantity': quantity,
        'customizations': customizations
    }
    
    session['cart'].append(cart_item)
    session.modified = True
    
    return jsonify({'status': 'success', 'cart_count': len(session['cart'])})

@main.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != cart_item_id]
        session.modified = True
    return redirect(url_for('main.view_cart'))
    
@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('main.index'))
        
    total = sum([(i['base_price'] + sum([opt['price_change'] for opt in i['customizations']])) * i['quantity'] for i in cart])
    
    # We assume one restaurant per order for simplicity, get from first item
    restaurant_id = cart[0]['restaurant_id']
    
    if request.method == 'POST':
        # Create order
        order = Order(
            user_id=current_user.id,
            restaurant_id=restaurant_id,
            total_amount=total,
            status='PAID'
        )
        db.session.add(order)
        db.session.flush()
        
        for item in cart:
            total_item_price = item['base_price'] + sum([opt['price_change'] for opt in item['customizations']])
            order_item = OrderItem(
                order_id=order.id,
                item_id=item['item_id'],
                quantity=item['quantity'],
                price_at_order=total_item_price
            )
            db.session.add(order_item)
            db.session.flush()
            
            for opt in item['customizations']:
                opt_id = opt['id']
                if str(opt_id).startswith('d_opt'):
                    grp = CustomizationGroup.query.filter_by(item_id=item['item_id'], name='Extra Toppings (Default)').first()
                    if not grp:
                        grp = CustomizationGroup(item_id=item['item_id'], name='Extra Toppings (Default)', type='multiple')
                        db.session.add(grp)
                        db.session.flush()
                    
                    real_opt = CustomizationOption.query.filter_by(group_id=grp.id, name=opt['name']).first()
                    if not real_opt:
                        real_opt = CustomizationOption(group_id=grp.id, name=opt['name'], price_change=opt['price_change'], icon=opt.get('icon', ''))
                        db.session.add(real_opt)
                        db.session.flush()
                    opt_id = real_opt.id
                    
                oic = OrderItemCustomization(
                    order_item_id=order_item.id,
                    option_id=int(opt_id)
                )
                db.session.add(oic)
                
        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            status='Completed'
        )
        db.session.add(payment)
        db.session.commit()
        session['cart'] = [] # clear cart
        session.modified = True

        flash('Order placed successfully! Delivery partners can now pick it up.', 'success')
        return redirect(url_for('customer.my_orders'))
        
    return render_template('main/checkout.html', cart=cart, total=total)

@main.route('/pay/<int:order_id>', methods=['GET', 'POST'])
@login_required
def pay(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if request.method == 'POST':
        # Simulate payment
        order.status = 'PAID'
        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            status='Completed'
        )
        db.session.add(payment)
        db.session.commit()
        flash('Payment successful! Your order is being prepared.', 'success')
        return redirect(url_for('customer.my_orders'))
        
    return render_template('main/pay.html', order=order)
