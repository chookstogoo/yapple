import sqlite3
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            isbn TEXT UNIQUE,
            quantity INTEGER,
            available_quantity INTEGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            transaction_type TEXT,
            transaction_date TEXT,
            due_date TEXT
        )''')

        # AUTO-MIGRATION: Safely add the 'status' column if missing
        try:
            cursor.execute("SELECT status FROM transactions LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE transactions ADD COLUMN status TEXT DEFAULT 'Active'")

        # AUTO-MIGRATION & DATA FIX: Safely add the 'quantity' column and clean up glitchy UI data
        try:
            cursor.execute("SELECT quantity FROM transactions LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE transactions ADD COLUMN quantity INTEGER DEFAULT 1")
            cursor.execute("""
                UPDATE transactions 
                SET quantity = CAST(transaction_type AS INTEGER), 
                    transaction_type = 'Request' 
                WHERE status = 'Pending' AND transaction_type != 'Request'
            """)

        conn.commit()
        conn.close()

    # --- User Methods ---
    def register_user(self, username, password, role):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, password, role))
            conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Username already exists")
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    # --- Book Methods ---
    def get_all_books(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books

    def add_book(self, title, author, isbn, quantity):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO books (title, author, isbn, quantity, available_quantity)
                          VALUES (?, ?, ?, ?, ?)''', (title, author, isbn, quantity, quantity))
        conn.commit()
        conn.close()

    def update_book(self, book_id, title, author, isbn, quantity):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity, available_quantity FROM books WHERE book_id=?", (book_id,))
        row = cursor.fetchone()
        if row:
            diff = quantity - row['quantity']
            new_avail = row['available_quantity'] + diff
            cursor.execute('''UPDATE books SET title=?, author=?, isbn=?, quantity=?, available_quantity=?
                              WHERE book_id=?''', (title, author, isbn, quantity, new_avail, book_id))
        conn.commit()
        conn.close()

    def delete_book(self, book_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
        conn.commit()
        conn.close()

    # --- Standard Transactions ---
    def get_all_transactions(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.transaction_id, u.username, b.title, t.transaction_type,
                                 t.transaction_date, t.due_date, t.quantity, t.status
                          FROM transactions t
                          JOIN users u ON t.user_id = u.user_id
                          JOIN books b ON t.book_id = b.book_id
                          ORDER BY t.transaction_date DESC''')
        trans = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return trans

    def get_user_borrowed_books(self, user_id):
        """Returns all transactions for the user by user ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.transaction_id, b.title, t.transaction_date, t.due_date,
                                 b.book_id, t.transaction_type, t.status, t.quantity, b.isbn AS barcode
                          FROM transactions t
                          JOIN books b ON t.book_id = b.book_id
                          WHERE t.user_id=? ORDER BY t.transaction_date DESC''', (user_id,))
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books

    def get_active_transactions(self, username):
        """Returns active AND returned transactions for the student view (by username)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.transaction_id, b.title, t.transaction_date, t.due_date,
                                 b.book_id, t.transaction_type, t.status, t.quantity, b.isbn AS barcode
                          FROM transactions t
                          JOIN books b ON t.book_id = b.book_id
                          JOIN users u ON t.user_id = u.user_id
                          WHERE u.username=? AND t.status IN ('Active', 'Returned', 'Pending') 
                          ORDER BY t.transaction_date DESC''', (username,))
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books

    # --- Book Request & Approval Logic ---
    def add_book_request(self, user_id, book_id, qty):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT title, available_quantity FROM books WHERE book_id=?", (book_id,))
        row = cursor.fetchone()
        if row:
            current_stock = row['available_quantity']
            selected_book_title = row['title']
            requested_qty = int(qty)

            if requested_qty > current_stock:
                from tkinter import messagebox
                messagebox.showerror("Stock Error",
                                     f"Cannot borrow {requested_qty}. Only {current_stock} copies of '{selected_book_title}' are available!")
                conn.close()
                return
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "Book not found in the database.")
            conn.close()
            return

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''INSERT INTO transactions (user_id, book_id, transaction_type, transaction_date, status, quantity)
                          VALUES (?, ?, 'Request', ?, 'Pending', ?)''',
                       (user_id, book_id, date_now, requested_qty))
        conn.commit()
        conn.close()

    def request_books(self, user_id, cart):
        for item in cart:
            self.add_book_request(user_id, item['book_id'], item['qty'])

    def get_pending_requests(self):
        """Returns pending requests + the ISBN so Barcodes load properly."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.transaction_id,
                                 t.user_id,
                                 t.book_id,
                                 u.username,
                                 b.title,
                                 t.quantity AS qty_requested,
                                 t.transaction_date,
                                 b.isbn AS barcode
                          FROM transactions t
                          JOIN users u ON t.user_id = u.user_id
                          JOIN books b ON t.book_id = b.book_id
                          WHERE t.status = 'Pending'
                          ORDER BY t.transaction_date ASC''')
        reqs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reqs

    def admin_approve_request(self, transaction_id, user_id, book_id, qty_requested):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            qty = int(qty_requested)
        except (ValueError, TypeError):
            qty = 1

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        cursor.execute("UPDATE transactions SET status='Approved' WHERE transaction_id=?",
                       (transaction_id,))

        cursor.execute('''INSERT INTO transactions
                          (user_id, book_id, transaction_type, transaction_date, due_date, status, quantity)
                          VALUES (?, ?, 'borrowed', ?, ?, 'Active', ?)''',
                       (user_id, book_id, date_now, due_date, qty))

        cursor.execute("UPDATE books SET available_quantity = available_quantity - ? WHERE book_id=?",
                       (qty, book_id))

        conn.commit()
        conn.close()

    def update_request_status(self, req_id, status):
        """Fix for Rejecting items."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE transactions SET status=? WHERE transaction_id=?", (status, req_id))
        conn.commit()
        conn.close()

    def return_book(self, transaction_id, book_id, quantity_str):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            qty = int(quantity_str)
        except ValueError:
            qty = 1

        # Marks the Active query as Returned, solving the missing log bug
        cursor.execute("UPDATE transactions SET status='Returned', transaction_type='RETURN' WHERE transaction_id=?",
                       (transaction_id,))
        cursor.execute("UPDATE books SET available_quantity = available_quantity + ? WHERE book_id=?",
                       (qty, book_id))
        conn.commit()
        conn.close()