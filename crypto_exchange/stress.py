import random
from datetime import datetime, timedelta
import psycopg2
import os 
from dotenv import load_dotenv 

user_ids = [11, 12]
order_types = ['buy', 'sell']
coins = ['BTC']

dotenv_path = os.path.join(os.path.dirname(__file__), 'crypto_exchange' ,'.env')
print(dotenv_path) 

load_dotenv(dotenv_path) 

db_host = os.getenv('PGHOST')  
db_name = os.getenv('PGDATABASE')
db_user = os.getenv('PGUSER')
db_password = os.getenv('PGPASSWORD')
print(db_host)
print(db_name)
print(db_user)
print(db_password)
# exit()
orders = []
for _ in range(200):
    type = random.choice(order_types)
    coin = random.choice(coins)
    price = random.randint(90, 150)  
    quantity = random.randint(1, 20) 
    user_id = random.choice(user_ids)
    created_at = datetime.now() - timedelta(days=random.randint(0, 30))  
    created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
    status = 'open'

    
    orders.append((type, price, quantity, coin, user_id, created_at_str, status))


try:

    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()


    insert_query = """
        INSERT INTO orders (type, price, quantity, coin, user_id, created_at, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    

    cursor.executemany(insert_query, orders)


    conn.commit()

    cursor.close()
    conn.close()

    print("Orders have been inserted into the database successfully.")
    
except Exception as e:
    print(f"An error occurred: {e}")
