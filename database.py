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
                                 t.transaction_date, t.due_date
                          FROM transactions t
                          JOIN users u ON t.user_id = u.user_id
                          JOIN books b ON t.book_id = b.book_id
                          ORDER BY t.transaction_date DESC''')
        trans = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return trans

    def get_user_borrowed_books(self, user_id):
        """
        Returns all non-returned transactions for the user (Pending requests + Active borrows).
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.transaction_id, b.title, t.transaction_date, t.due_date,
                                 b.book_id, t.transaction_type, t.status
                          FROM transactions t
                          JOIN books b ON t.book_id = b.book_id
                          WHERE t.user_id=? AND t.status IN ('Pending', 'Active')''', (user_id,))
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books

    # --- Book Request & Approval Logic ---

    def add_book_request(self, user_id, book_id, qty):
        """Insert a single pending book request for a student."""
        conn = self.get_connection()
        cursor = conn.cursor()
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''INSERT INTO transactions (user_id, book_id, transaction_type, transaction_date, status)
                          VALUES (?, ?, ?, ?, 'Pending')''',
                       (user_id, book_id, str(qty), date_now))
        conn.commit()
        conn.close()

    def request_books(self, user_id, cart):
        """
        Submit multiple book requests from the student cart.
        cart is a list of dicts: [{'book_id': int, 'title': str, 'qty': int}, ...]
        """
        for item in cart:
            self.add_book_request(user_id, item['book_id'], item['qty'])

    def get_pending_requests(self):
        """
        Returns all pending book requests with all fields needed by the admin dashboard.
        Keys: transaction_id, user_id, book_id, username, title, qty_requested, transaction_date
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.transaction_id,
                                 t.user_id,
                                 t.book_id,
                                 u.username,
                                 b.title,
                                 t.transaction_type AS qty_requested,
                                 t.transaction_date
                          FROM transactions t
                          JOIN users u ON t.user_id = u.user_id
                          JOIN books b ON t.book_id = b.book_id
                          WHERE t.status = 'Pending'
                          ORDER BY t.transaction_date ASC''')
        reqs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reqs

    def admin_approve_request(self, transaction_id, user_id, book_id, qty_requested):
        """
        Approve a pending request:
        1. Mark the pending transaction as 'Approved'
        2. Insert a new 'borrowed' / 'Active' transaction with a due date
        3. Decrement available_quantity on the book
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            qty = int(qty_requested)
        except (ValueError, TypeError):
            qty = 1

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        # Mark the request row as Approved
        cursor.execute("UPDATE transactions SET status='Approved' WHERE transaction_id=?",
                       (transaction_id,))

        # Create the actual borrow record
        cursor.execute('''INSERT INTO transactions
                          (user_id, book_id, transaction_type, transaction_date, due_date, status)
                          VALUES (?, ?, 'borrowed', ?, ?, 'Active')''',
                       (user_id, book_id, date_now, due_date))

        # Reduce available stock
        cursor.execute("UPDATE books SET available_quantity = available_quantity - ? WHERE book_id=?",
                       (qty, book_id))

        conn.commit()
        conn.close()

    def update_request_status(self, req_id, status):
        """Legacy helper kept for compatibility."""
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
        cursor.execute("UPDATE transactions SET status='Returned' WHERE transaction_id=?", (transaction_id,))
        cursor.execute("UPDATE books SET available_quantity = available_quantity + ? WHERE book_id=?",
                       (qty, book_id))
        conn.commit()
        conn.close()