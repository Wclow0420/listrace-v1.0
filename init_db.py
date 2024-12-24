import sqlite3

DATABASE = 'app_data.db'  # SQLite database file

def init_db():
    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create the tables if they don't already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Buildings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location_id INTEGER,
        FOREIGN KEY(location_id) REFERENCES Locations(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Houses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        building_id INTEGER,
        FOREIGN KEY(building_id) REFERENCES Buildings(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        house_id INTEGER,
        FOREIGN KEY(house_id) REFERENCES Houses(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tenants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT,
        email TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RentDetails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER,
        room_id INTEGER,
        rent_amount DECIMAL(10, 2),
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY(tenant_id) REFERENCES Tenants(id),
        FOREIGN KEY(room_id) REFERENCES Rooms(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PaymentRecords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rent_id INTEGER,
        payment_amount DECIMAL(10, 2),
        payment_date TEXT,
        FOREIGN KEY(rent_id) REFERENCES RentDetails(id)
    );
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

# Run the function to create the database and tables
if __name__ == '__main__':
    init_db()
