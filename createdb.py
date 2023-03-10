import sqlite3

conn = sqlite3.connect('products.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        details TEXT,
        picture BLOB
    )
''')

conn.commit()
conn.close()
