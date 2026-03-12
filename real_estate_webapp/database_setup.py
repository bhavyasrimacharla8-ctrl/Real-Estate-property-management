import sqlite3

# Create new database file
conn = sqlite3.connect('realestate.db')
cursor = conn.cursor()

# Create Owners table
cursor.execute("""
CREATE TABLE Owners (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

# Create Locations table
cursor.execute("""
CREATE TABLE Locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    city TEXT,
    state TEXT
)
""")

# Create Properties table
cursor.execute("""
CREATE TABLE Properties (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner_id INTEGER,
    location_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES Owners(owner_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
)
""")

# Insert sample data
cursor.execute("INSERT INTO Owners (name, phone, email) VALUES ('Ramesh Kumar', '9876543210', 'ramesh@gmail.com')")
cursor.execute("INSERT INTO Locations (address, city, state) VALUES ('Madhapur', 'Hyderabad', 'Telangana')")
cursor.execute("INSERT INTO Properties (name, owner_id, location_id) VALUES ('Green Villa', 1, 1)")

conn.commit()
conn.close()

print("Database created successfully!")

cursor.execute("""
CREATE TABLE IF NOT EXISTS agents(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
)
""")