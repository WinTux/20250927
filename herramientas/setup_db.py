import sqlite3

conn = sqlite3.connect('taller.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    INSERT OR IGNORE INTO usuarios (username, password)
    VALUES (?, ?)
''', ('usuario1', '123456'))

cursor.execute('''
    INSERT OR IGNORE INTO usuarios (username, password)
    VALUES (?, ?)
''', ('usuario2', '654321'))

conn.commit()
conn.close()

print("Base de datos creada con éxito.")
