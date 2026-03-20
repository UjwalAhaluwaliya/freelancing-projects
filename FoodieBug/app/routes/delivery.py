from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Order
from app.utils.decorators import role_required

delivery = Blueprint('delivery', __name__)

@delivery.route('/dashboard')
@login_required
@role_required('DeliveryPartner')
def dashboard():
    # Orders that are paid, ready or preparing and have NO delivery partner yet
    available_orders = Order.query.filter(Order.status.in_(['PAID', 'Preparing', 'Ready']), Order.delivery_partner_id == None).all()
    
    # Orders currently assigned to this delivery partner
    my_active_orders = Order.query.filter_by(delivery_partner_id=current_user.id, status='Out for Delivery').all()
    
    # Delivered orders by this delivery partner
    my_completed_orders = Order.query.filter_by(delivery_partner_id=current_user.id, status='Delivered').order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('delivery/dashboard.html', 
                           available_orders=available_orders, 
                           my_active_orders=my_active_orders,
                           my_completed_orders=my_completed_orders)

@delivery.route('/accept/<int:order_id>', methods=['POST'])
@login_required
@role_required('DeliveryPartner')
def accept(order_id):
    order = Order.query.get_or_404(order_id)
    if order.delivery_partner_id is None:
        order.delivery_partner_id = current_user.id
        order.status = 'Out for Delivery'
        db.session.commit()
        flash('Order accepted! Please pick it up from the restaurant.', 'success')
    else:
        flash('This order was already accepted by someone else.', 'danger')
    return redirect(url_for('delivery.dashboard'))

@delivery.route('/map/<int:order_id>')
@login_required
@role_required('DeliveryPartner')
def map_view(order_id):
    order = Order.query.get_or_404(order_id)
    if order.delivery_partner_id != current_user.id:
        flash('You are not assigned to this order.', 'danger')
        return redirect(url_for('delivery.dashboard'))
        
    return render_template('delivery/map.html', order=order)

@delivery.route('/deliver/<int:order_id>', methods=['POST'])
@login_required
@role_required('DeliveryPartner')
def deliver(order_id):
    order = Order.query.get_or_404(order_id)
    if order.delivery_partner_id == current_user.id and order.status == 'Out for Delivery':
        order.status = 'Delivered'
        db.session.commit()
        flash('Order marked as Delivered! Great job.', 'success')
    return redirect(url_for('delivery.dashboard'))
