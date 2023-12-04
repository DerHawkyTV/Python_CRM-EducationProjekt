import sqlite3

class Database:
    def __init__(self, db_file='crm_database.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                birthdate TEXT,
                notes TEXT
            )
        ''')
        self.conn.commit()

    def add_customer(self, name, email, phone, address, birthdate, notes):
        self.cursor.execute('INSERT INTO customers (name, email, phone, address, birthdate, notes) VALUES (?, ?, ?, ?, ?, ?)',
                            (name, email, phone, address, birthdate, notes))
        self.conn.commit()

    def edit_customer(self, customer_id, name, email, phone, address, birthdate, notes):
        self.cursor.execute('''
            UPDATE customers 
            SET name=?, email=?, phone=?, address=?, birthdate=?, notes=? 
            WHERE id=?
        ''', (name, email, phone, address, birthdate, notes, customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id):
        self.cursor.execute('DELETE FROM customers WHERE id=?', (customer_id,))
        self.conn.commit()

    def get_all_customers(self):
        self.cursor.execute('SELECT * FROM customers')
        return self.cursor.fetchall()

    def get_stats_by_region(self):
        # Beispiel: Anzahl der Kunden pro Region
        self.cursor.execute('SELECT address, COUNT(*) FROM customers GROUP BY address')
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
