import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()


# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS mood (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    mood TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    comment TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
)
''')

# Insert sample data
mood = [
    ('1', 'John Doe', 'john@doe.co.nz', 'happy', '2023-10-01 10:00:00', 'Feeling great today!'),
    ('2' ,'Jane Smith', 'jane@smith.co.nz', 'sad', '2023-10-01 11:00:00', 'A bit down, but hopeful.'),
]

cursor.executemany('INSERT INTO mood (account_id, name, email, mood, timestamp, comment) VALUES (?, ?, ?, ?, ?, ?)', mood)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created successfully with sample data.")