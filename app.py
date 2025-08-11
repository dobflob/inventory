from models import Base, session, Product, engine
import csv
from datetime import date, datetime
from time import sleep

def clean_price(price):
    price = price[1:]
    try:
        return int(float(price) * 100)
    except ValueError:
        msg = f'Invalid price. Try again.'
        # add function call to print error message


def clean_quantity(quantity):
    try:
        return int(quantity)
    except ValueError:
        msg = f'Invalid quantity. Try again.'
        # add function call to print error message
    

def clean_date(updated_date):
    try:
        return datetime.strptime(updated_date, '%m/%d/%Y').date()
    except ValueError:
        msg = f'Invalid date format. Try again.'
        # add function call to print error message

def import_csv():
    with open('inventory.csv') as csvfile:
        data = csv.DictReader(csvfile)
        for record in data:
            record['product_price'] = clean_price(record['product_price'])
            record['product_quantity'] = clean_quantity(record['product_quantity'])
            record['date_updated'] = clean_date(record['date_updated'])
            add_product(record)


def add_product(product):
    existing_product = session.query(Product).filter(Product.product_name == product['product_name']).first()
    if existing_product:  # if product already exists
        # check date updated
        product_to_update = product if product['date_updated'] > existing_product.date_updated else None
        if product_to_update:  # only update if date is more recent
            existing_product.product_quantity = product['product_quantity']
            existing_product.product_price = product['product_price']
            existing_product.date_updated = product['date_updated']
    else:  # if product to add doesn't already exist
        product_to_add = Product(product_name=product['product_name'],product_quantity=product['product_quantity'],product_price=product['product_price'], date_updated=product['date_updated'])
        session.add(product_to_add)
    session.commit()


def main():
    import_csv()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    main()