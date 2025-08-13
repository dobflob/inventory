from models import Base, session, Product, engine
import csv
from datetime import datetime
from time import sleep


def display_error(msg):
    print(f'''
x  x  x  Error  x  x  x
-----------------------
{msg} Please try again.

''')
    sleep(1)


def clean_price(price):
    price = price[1:]
    try:
        return int(float(price) * 100)
    except ValueError:
        display_error('Invalid price.')


def clean_quantity(quantity):
    try:
        return int(quantity)
    except ValueError:
        display_error('Quantity must be a number.')
    

def clean_date(updated_date):
    try:
        return datetime.strptime(updated_date, '%m/%d/%Y').date()
    except ValueError:
        display_error('Invalid date format (MM/DD/YYYY).')


def format_price(price):
    float_price = (price / 100)
    return f'{float_price:.2f}'


def format_date(updated_date):
    return updated_date.strftime('%m/%d/%Y')


def import_csv():
    with open('inventory.csv') as csvfile:
        data = csv.DictReader(csvfile)
        for record in data:
            record['product_price'] = clean_price(record['product_price'])
            record['product_quantity'] = clean_quantity(record['product_quantity'])
            record['date_updated'] = clean_date(record['date_updated'])
            add_product(record)


def backup_to_csv():
    headers = ['product_name', 'product_price', 'product_quantity', 'date_updated']
    products = session.query(Product).all()
    with open('backup.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for product in products:
            name = product.product_name
            quantity = product.product_quantity
            price = format_price(product.product_price)
            updated = format_date(product.date_updated)
            writer.writerow([name, quantity, price, updated])


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


def get_product_by_id():
    while True:
        id = input('>> Product Id:  ')
        product = session.query(Product).filter(Product.product_id==id).first()
        if product:
            return product
        else:
            display_error('Product not found.')


def new_product():
    new_product = {}
    name_error = True
    while name_error:
        name = input('>> Product Name:  ').title()
        if len(name) > 2:
            new_product['product_name'] = name
            name_error = False
        else:
            display_error('Name must be at least 3 characters.')
    qty_error = True
    while qty_error:
        quantity = clean_quantity(input('>> Quantity:  '))
        if quantity:
            new_product['product_quantity'] = quantity
            qty_error = False
    price_error = True
    while price_error:
        price = clean_price('$' + input('>> Price (e.g. 3.99):  $'))
        if price:
            new_product['product_price'] = price
            price_error = False
    updated_error = True
    while updated_error:
        updated = clean_date(input(f'>> Date Updated (e.g. 4/10/2025):  '))
        if updated:
            new_product['date_updated'] = updated
            updated_error = False
    return new_product


def menu():
    print('''
    Main Menu
-----------------
v - View Product
a - Add Product
b - Backup Data
''')
    return input('>> What do you want to do? (Enter to quit)  ')


def main():
    import_csv()
    while True:
        choice = menu()
        if choice not in ('vab'):
            display_error('Invalid selection.')
        elif choice.lower() == 'v':
            product = get_product_by_id()
            print(product)
            sleep(1)
        elif choice.lower() == 'a':
            product = new_product()
            add_product(product)
            print(f'\n{product['product_name'].title()} added successfully.')
            sleep(1)
        elif choice.lower() == 'b':
            backup_to_csv()
        else:
            break
        

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    main()