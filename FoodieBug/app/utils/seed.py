from app import db, bcrypt
from app.models import User, Restaurant, MenuItem, CustomizationGroup, CustomizationOption

def seed_data():
    if User.query.first():
        print("Data already seeded. Skipping...")
        return

    # Create Users
    admin_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
    sys_admin = User(name='System Admin', email='admin@foodiebug.com', password=admin_pw, role='SystemAdmin')
    
    rest_pw = bcrypt.generate_password_hash('rest123').decode('utf-8')
    rest_admin = User(name='Burger King Admin', email='bk@foodiebug.com', password=rest_pw, role='RestaurantAdmin')
    
    cust_pw = bcrypt.generate_password_hash('cust123').decode('utf-8')
    customer = User(name='John Doe', email='john@example.com', password=cust_pw, role='Customer')
    
    db.session.add_all([sys_admin, rest_admin, customer])
    db.session.flush() # To get user IDs

    # Create Restaurant
    restaurant = Restaurant(name='Burger King', location='123 Fast Food Lane', contact='1800-BURGER', user_id=rest_admin.id)
    db.session.add(restaurant)
    db.session.flush()

    # Create Menu Items
    burger = MenuItem(restaurant_id=restaurant.id, name='Whopper', description='Flame-grilled beef patty, topped with tomatoes, fresh cut lettuce, mayo, pickles, a swirl of ketchup, and sliced white onions.', base_price=5.99)
    fries = MenuItem(restaurant_id=restaurant.id, name='French Fries', description='More delicious than ever, our signature piping hot, thick cut Salted French Fries are golden on the outside and fluffy on the inside.', base_price=2.49)
    
    db.session.add_all([burger, fries])
    db.session.flush()

    # Customization Groups for Burger
    cheese_grp = CustomizationGroup(item_id=burger.id, name='Add Cheese', type='single')
    bacon_grp = CustomizationGroup(item_id=burger.id, name='Add Extras', type='multiple')
    db.session.add_all([cheese_grp, bacon_grp])
    db.session.flush()

    # Customization Options
    opt1 = CustomizationOption(group_id=cheese_grp.id, name='No Cheese', price_change=0, icon='🚫')
    opt2 = CustomizationOption(group_id=cheese_grp.id, name='American Cheese', price_change=0.50, icon='🧀')
    opt3 = CustomizationOption(group_id=cheese_grp.id, name='Swiss Cheese', price_change=0.60, icon='🧀')
    
    opt4 = CustomizationOption(group_id=bacon_grp.id, name='Extra Bacon', price_change=1.50, icon='🥓')
    opt5 = CustomizationOption(group_id=bacon_grp.id, name='Jalapeños', price_change=0.50, icon='🌶️')
    
    # Customization Group for Fries
    size_grp = CustomizationGroup(item_id=fries.id, name='Size', type='single')
    db.session.add(size_grp)
    db.session.flush()
    
    opt6 = CustomizationOption(group_id=size_grp.id, name='Small', price_change=0, icon='🍟')
    opt7 = CustomizationOption(group_id=size_grp.id, name='Medium', price_change=0.50, icon='🍟')
    opt8 = CustomizationOption(group_id=size_grp.id, name='Large', price_change=1.00, icon='🍟')

    db.session.add_all([opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8])
    
    db.session.commit()
    print("Database seeded successfully with demo data.")
