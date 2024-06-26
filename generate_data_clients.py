import psycopg2
from faker import Faker
import uuid  # Module pour générer des UUID uniques

fake = Faker()

def create_clients_table(conn):
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        address TEXT,
        email VARCHAR(100),
        phone VARCHAR(20),
        username VARCHAR(50),
        password VARCHAR(100)  -- Augmentez la taille si nécessaire
    )
    ''')
    conn.commit()
    cur.close()

def generate_clients(n):
    clients = []
    for _ in range(n):
        client = (
            fake.first_name(),
            fake.last_name(),
            fake.address(),
            fake.email(),
            fake.phone_number()[:20],  # Tronquer le numéro de téléphone à 20 caractères
            fake.user_name(),
            str(uuid.uuid4())[:12]  # Générer un mot de passe unique (UUID tronqué à 12 caractères)
        )
        clients.append(client)
    return clients

def insert_clients_data(conn, clients):
    cur = conn.cursor()
    
    cur.executemany('''
    INSERT INTO clients (first_name, last_name, address, email, phone, username, password) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', clients)
    
    conn.commit()
    cur.close()

def main():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="clients_db",
            user="user",
            password="password",
            host="localhost",
            port="5435",
            client_encoding="utf-8"  # Spécifiez l'encodage client
        )

        create_clients_table(conn)  # Créez la table clients si elle n'existe pas
        clients = generate_clients(100)  # Générer 100 clients factices avec username et mot de passe uniques
        insert_clients_data(conn, clients)  # Insérer les données générées
        print("Data inserted successfully.")
    
    except psycopg2.Error as e:
        print(f"Error: {e}")
    
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()
