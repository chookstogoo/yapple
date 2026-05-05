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

        # Added status column to transactions
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            transaction_type TEXT,
            transaction_date TEXT,
            due_date TEXT,
            status TEXT
        )''')

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
        cursor.execute('''SELECT t.transaction_id, u.username, b.title, t.transaction_type, t.transaction_date, t.due_date
                          FROM transactions t
                          JOIN users u ON t.user_id = u.user_id
                          JOIN books b ON t.book_id = b.book_id
                          ORDER BY t.transaction_date DESC''')
        trans = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return trans

    def get_user_borrowed_books(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        # Added t.status and updated WHERE clause to show Pending requests
        cursor.execute('''SELECT t.transaction_id, b.title, t.transaction_date, t.due_date, b.book_id, t.transaction_type, t.status
                          FROM transactions t
                          JOIN books b ON t.book_id = b.book_id
                          WHERE t.user_id=? AND t.status IN ('Pending', 'Active', 'Rejected') ''', (user_id,))
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books

    # --- Book Request & Approval Logic ---
    def add_book_request(self, user_id, book_id, qty):
        """Called by StudentDashboard to request a book."""
        conn = self.get_connection()
        cursor = conn.cursor()
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # We store the requested quantity in the transaction_type column temporarily
        cursor.execute('''INSERT INTO transactions (user_id, book_id, transaction_type, transaction_date, status)
                          VALUES (?, ?, ?, ?, 'Pending')''',
                       (user_id, book_id, str(qty), date_now))
        conn.commit()
        conn.close()

    def get_pending_requests(self):
        """Called by AdminDashboard to view pending requests."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT t.transaction_id as request_id, u.username, b.title, 
                                 t.transaction_type as qty, t.status
                          FROM transactions t
                          JOIN users u ON t.user_id = u.user_id
                          JOIN books b ON t.book_id = b.book_id
                          WHERE t.status = 'Pending' ''')
        reqs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reqs

    def update_request_status(self, req_id, status):
        """Called by AdminDashboard to approve or reject a request."""
        conn = self.get_connection()
        cursor = conn.cursor()

        if status == "Approved":
            # 1. Get the original request details
            cursor.execute("SELECT user_id, book_id, transaction_type FROM transactions WHERE transaction_id=?",
                           (req_id,))
            req = cursor.fetchone()

            if req:
                user_id = req['user_id']
                book_id = req['book_id']
                try:
                    qty = int(req['transaction_type'])
                except ValueError:
                    qty = 1

                date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

                # 2. Mark original request as Approved
                cursor.execute("UPDATE transactions SET status='Approved' WHERE transaction_id=?", (req_id,))

                # 3. Create a new Active transaction for the checked-out book
                cursor.execute('''INSERT INTO transactions (user_id, book_id, transaction_type, transaction_date, due_date, status)
                                  VALUES (?, ?, 'borrowed', ?, ?, 'Active')''',
                               (user_id, book_id, date_now, due_date))

                # 4. Deduct inventory
                cursor.execute("UPDATE books SET available_quantity = available_quantity - ? WHERE book_id=?",
                               (qty, book_id))
        else:
            # If "Rejected", simply update the status
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
        cursor.execute("UPDATE books SET available_quantity = available_quantity + ? WHERE book_id=?", (qty, book_id))

        conn.commit()
        conn.close()