import psycopg2
import random
from faker import Faker

fake = Faker()

def generate_orders(n, client_count, product_count):
    orders = []
    for _ in range(n):
        order = (
            random.randint(1, client_count),  # client_id
            random.randint(1, product_count),  # product_id
            fake.date_between(start_date='-1y', end_date='today'),  # order_date
            fake.date_between(start_date='today', end_date='+30d'),  # delivery_date
            random.randint(1, 10)  # quantity
        )
        orders.append(order)
    return orders

def insert_orders_data(conn, orders):
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        client_id INTEGER,
        product_id INTEGER,
        order_date DATE,
        delivery_date DATE,
        quantity INTEGER
    )
    ''')
    
    cur.executemany('''
    INSERT INTO orders (client_id, product_id, order_date, delivery_date, quantity) 
    VALUES (%s, %s, %s, %s, %s)
    ''', orders)
    
    conn.commit()
    cur.close()

def main():
    conn = psycopg2.connect(
        dbname="orders_db",
        user="user",
        password="password",
        host="localhost",
        port="5437" 
    )
    
    # Generate orders assuming we have 100 clients and 10 products
    orders = generate_orders(200, 100, 10)
    insert_orders_data(conn, orders)
    
    conn.close()

if __name__ == "__main__":
    main()
