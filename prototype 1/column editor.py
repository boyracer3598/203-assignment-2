import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

# Add a new column to an existing table
cursor.execute("ALTER TABLE accounts ADD COLUMN excerised INTEGER DEFAULT 0")

conn.commit()
conn.close()
