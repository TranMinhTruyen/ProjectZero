from sqlalchemy import Column, Integer, String, Float, Date , ForeignKey
from sqlalchemy.orm import relationship, backref

from app.common.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), index=True)
    price = Column(Float, index=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    order = relationship("OrderDetail")
    cart = relationship("Cart")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), index=True)

    products = relationship("Product")


class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), index=True)

    product = relationship("Product")


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String(225), nullable=False)
    password = Column(String(225), nullable=False)
    firstname = Column(String(20), nullable=True)
    lastname = Column(String(20), nullable=True)
    birthday = Column(Date, nullable=True)
    phonenumber = Column(Integer, nullable=True)
    andress = Column(String(225), nullable=True)
    is_active = Column(String(10), nullable=False)

    order = relationship("Order")
    customercart = relationship("Cart")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String(225), nullable=False)
    password = Column(String(225), nullable=False)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    citizen_id = Column(Integer, nullable=False)
    phonenumber = Column(Integer, nullable=False)
    andress = Column(String(225), nullable=False)
    is_active = Column(String(10), nullable=False)

    order = relationship("Order")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    create_day = Column(Date, nullable=False)
    phonenumber = Column(Integer, nullable=False)
    andress = Column(String(225), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(10), nullable=False)
    description = Column(String(225), nullable=True)

    customer_id = Column(Integer, ForeignKey('customer.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    product = relationship("OrderDetail")

class OrderDetail(Base):
    __tablename__ = "orderdetail"

    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    total = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    product = relationship("Product")
    order = relationship("Order")


class Cart(Base):

    __tablename__ = "cart"
    customer_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    total = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    customer = relationship("Customer")
    product = relationship("Product")