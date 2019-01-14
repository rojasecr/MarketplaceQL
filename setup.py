from ast import literal_eval
from models import engine, db_session, Base, Product
import sys

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

    with open('fruits.json', 'r') as file:
        data = literal_eval(file.read())
        for record in data:
            product = Product(**record)
            db_session.add(product)
        db_session.commit()
