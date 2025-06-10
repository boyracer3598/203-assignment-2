import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT
)
''')

# Insert sample data
accounts = [
    ('John Doe', 'john@doe.co.nz', '12345678'),
    ('Jane Smith', 'jane@smith.co.nz', '87654321'),
    ('Bob Johnson', 'bob@johnson.co.nz', 'password123')
]

cursor.executemany('INSERT INTO accounts (name, email, password) VALUES (?, ?, ?)', accounts)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created successfully with sample data.")