import psycopg2
import random

def generate_products(n):
    products = []
    for i in range(n):
        product = (
            f"Capsule {i+1}",
            round(random.uniform(0.5, 5.0), 2),  # price between 0.5 and 5.0
            random.randint(0, 100)  # availability between 0 and 100
        )
        products.append(product)
    return products

def insert_products_data(conn, products):
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        price DECIMAL(5, 2),
        availability INTEGER
    )
    ''')
    
    cur.executemany('''
    INSERT INTO products (name, price, availability) 
    VALUES (%s, %s, %s)
    ''', products)
    
    conn.commit()
    cur.close()

def main():
    conn = psycopg2.connect(
        dbname="products_db",
        user="user",
        password="password",
        host="localhost",
        port="5436" 
    )
    
    products = generate_products(10)
    insert_products_data(conn, products)
    
    conn.close()

if __name__ == "__main__":
    main()
