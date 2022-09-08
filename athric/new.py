#!/usr/bin/env python
"""
This module is for my flask app
Implementing the studies from flask course
"""
from flask import Flask
# from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random

# fake = Faker()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print('Obed Amoako')

class Customer(db.Model):
    """Customer table"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    # last_name = db.Column(db.String(50), nullable=False)
    # address = db.Column(db.String(500), nullable=False)
    # city = db.Column(db.String(50), nullable=False)
    # postcode = db.Column(db.String(50), nullable=False)
    # email = db.Column(db.String(50), nullable=False, unique=True)

    orders = db.relationship('Order', backref='customer')

order_product = db.Table('order_product', 
    db.Column(' order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


class Product(db.Model):
    """The Product table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    """Orders Table"""
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    products = db.relationship('Product', secondary='order_product')

db.create_all()

                        ########### DRIVER CODE ############
def add_customers():
    for _ in range(100):
        customer = Customer(
            first_name='Obed',
            # last_name=fake.last_name(),
            # address=fake.street_address(),
            # city=fake.city(),
            # postcode=fake.postcode(),
            # email=fake.email()
        )
        db.session.add(customer)
    db.session.commit()

def add_orders():
    """ Create New Orders """
    customers = Customer.query.all()

    for _ in range(1000):
        #choose a random customer
        customer = random.choice(customers)

        # ordered_date = fake.date_time_this_year()
        # shipped_date = random.choices([None, fake.date_time_between(start_date=ordered_date)], [10, 90])[0]

        #choose either random None or random date for delivered and shipped
        delivered_date = None
        # if shipped_date:
        #     delivered_date = random.choices([None, fake.date_time_between(start_date=shipped_date)], [50, 50])[0]

        #choose either random None or one of three coupon codes
        coupon_code = random.choices([None, '50OFF', 'FREESHIPPING', 'BUYONEGETONE'], [80, 5, 5, 5])[0]

        order = Order(
            customer_id=customer.id,
            # order_date=ordered_date,
            # shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code
        )

        db.session.add(order)
    db.session.commit()

def add_products():
    """ New products added """
    for _ in range(10):
        product = Product(
            # name=fake.color_name(),
            price=random.randint(10,100)
        )
        db.session.add(product)
    db.session.commit()

def add_order_products():
    """ create new order_product objects """
    orders = Order.query.all()
    products = Product.query.all()

    for order in orders:
        #select random k
        k = random.randint(1, 3)
        # select random products
        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)

    db.session.commit()

def create_random_data():
    """This one creates a new database with fake data"""
    db.create_all()
    add_customers()
    add_orders()
    add_products()
    add_order_products()

def get_orders_by(customer_id=1):
    """Gets all orders a customer has made"""
    customer_orders = Order.query.filter_by(customer_id=customer_id).all()
    print(f"{customer_orders[1].customer.first_name} made these orders")
    for order in customer_orders:
        print(order.id)


def get_pending_orders():
    """show all pending orders"""
    print("Here, The Pening Orders")
    pending_orders = Order.query.filter_by(
            shipped_date=None).order_by(Order.order_date.asc())
    for order in pending_orders:
        print(f"Id: {order.id}; Order date: {order.order_date}")


def how_many_customers():
    """Count the number of customers"""
    no_of_customers = (Customer.query.count())
    print(f"Current customers: {no_of_customers}")


def orders_with_coupon():
    """Get all orders with coupon code"""
    coupon_orders = Order.query.filter(Order.coupon_code.isnot(None))
    print("All orders with coupon")
    for order in coupon_orders:
        print(f"order: {order.id} has {order.coupon_code}")

def revenue_in_some_days(x=30):
    """Get the total revenue in last x days"""
    amount = db.session.query(db.func.sum(Product
        .price)).join(order_product).join(Order).filter(Order
                .order_date > (datetime.now() - timedelta(days=x))
        ).scalar()
    print(f"Revenue in last {x} days: ${amount}.00")


def average_fulfillment_time():
    """
    Shows the average time a
    customer is likely to receive his order
    """
    average = db.session.query(
            db.func.time(
                db.func.avg(
                    db.func.strftime('%s', Order
                        .shipped_date) - db.func.strftime('%s',
                        Order.order_date)), 'unixepoch')
        ).filter(Order.shipped_date.isnot(None)).scalar()
    print(f"Average time to get goods: {average}")


def customers_who_purchased_x(amount=500):
    """Gets all customers who have purchased at least @amount"""
    customers = db.session.query(Customer).join(
            Order).join(order_product).join(
                    Product).group_by(Customer).having(db.func.sum(Product
                        .price) >= amount)
    try:
        if customers[0]:
            print(f"The following customers have purchased", end=" ")
            print(f"more than {amount} Dollars")

            for customer in customers:
                print(f"{customer.first_name} {customer.last_name}")
    except IndexError:
        print(f'No one has yet purchased {amount} Dollars')
