from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import Order
from app.utils.decorators import role_required

customer = Blueprint('customer', __name__)

@customer.route('/my_orders')
@login_required
@role_required('Customer', 'SystemAdmin', 'RestaurantAdmin')
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/orders.html', orders=orders)
