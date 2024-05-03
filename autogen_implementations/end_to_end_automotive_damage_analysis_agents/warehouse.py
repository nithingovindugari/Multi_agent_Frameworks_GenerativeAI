import sqlite3

# Warehouse declaration for the automotive parts for function mapping
get_warehouse_declaration = {"name": "get_warehouse", "description": "Retrieves the warehose list"}



# Function to setup the database for the warehouse of automotive parts
def setup_db():
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS warehouse
                 ( part_id INTEGER PRIMARY KEY, part_name TEXT NOT NULL, 
                   quantity INTEGER NOT NULL, price INTEGER NOT NULL)''')
    
    print("Database setup complete for warehouse of automotive parts")
    conn.close()
    

# Function to add the automotive parts to the warehouse
def add_data():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()

    # Data to be added
    parts = [
        (1, 'Tesla Bumper', 10, 1000),
        (2, 'Tesla Display', 5, 2000),
        (3, 'Porsche Tires', 50, 750),
        (4, 'Tesla Wind shield', 40, 400),
        (5, 'Porsche bumper', 50, 500),
        (6, 'Tesla Frunk', 15, 1200),  
        (7, 'Tesla Hood', 20, 1500),  
        (8, 'Tesla Wheel', 60, 800), 
        (9, 'Tesla Internal Components', 30, 2500) 
    ]

    cursor.executemany('INSERT INTO warehouse VALUES (?, ?, ?, ?)', parts)

    conn.commit()
    print("Data added to the warehouse table successfully")
    conn.close()
    
# Function to fetch the automotive parts from the warehouse
def get_warehouse():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM warehouse")

    data = cursor.fetchall()
    
    warehouse_list = [{"part_id": part[0], "part_name": part[1], "quantity": part[2], "price": part[3]} for part in data]
    print("Parts in the warehouse:")

    conn.close()
    
    return warehouse_list

# setup_db()
# add_data()

# print(get_warehouse())