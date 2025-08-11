from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)

    def __repr__(self):
        return f'''
Name: {self.product_name}
Quantity: {self.product_quantity}
Price: ${self.product_price / 100}
Updated: {self.date_updated}      
'''


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    products = session.query(Product).all()
    if products:
        for product in products:
            print(product)
    else:
        print('No products found')