from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

# We will need this for querying
Base.query = db_session.query_property()

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    inventory_count = Column(Integer)


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    items = relationship("Item", uselist=True, cascade='delete,all', backref="cart")
    total = Column(Integer)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product") 


