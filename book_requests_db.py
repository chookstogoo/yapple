import sqlite3
from datetime import datetime

DB_NAME = "test_library_requests.db"


def init_test_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Available INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            book_id INTEGER,
            quantity INTEGER,
            status TEXT,
            date TEXT
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO books (Title, Available) VALUES (?, ?)", [
            ("AutoCAD 2023 Instructor", 10),
            ("Introduction to Algorithms", 4),
            ("Principle of Solid Mechanics", 67)
        ])

    conn.commit()
    conn.close()


def get_all_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Title, Available FROM books")
    books = cursor.fetchall()
    conn.close()
    return books


def request_books(user_id, cart_items):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_requested = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in cart_items:
        cursor.execute("SELECT Available, Title FROM books WHERE ID = ?", (item['book_id'],))
        result = cursor.fetchone()

        if result:
            current_stock = result[0]
            title = result[1]
            requested_qty = int(item['qty'])

            if requested_qty > current_stock:
                from tkinter import messagebox
                messagebox.showerror("Stock Error",
                                     f"Cannot borrow {requested_qty}. Only {current_stock} copies of '{title}' are available!")
                conn.close()
                return
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "Book not found in the database.")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO transactions (user_id, book_id, quantity, status, date) 
            VALUES (?, ?, ?, 'Pending', ?)
        """, (user_id, item['book_id'], item['qty'], date_requested))

    conn.commit()
    conn.close()


def get_pending_requests():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.user_id, b.Title, t.quantity, t.date, t.book_id
        FROM transactions t
        JOIN books b ON t.book_id = b.ID
        WHERE t.status = 'Pending'
    """)
    requests = cursor.fetchall()
    conn.close()
    return requests


def admin_approve_request(transaction_id, user_id, book_id, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("UPDATE transactions SET status = 'Approved' WHERE id = ?", (transaction_id,))
        cursor.execute("""
            INSERT INTO transactions (user_id, book_id, quantity, status, date) 
            VALUES (?, ?, ?, 'Active', ?)
        """, (user_id, book_id, quantity, date_now))
        cursor.execute("UPDATE books SET Available = Available - ? WHERE ID = ?", (quantity, book_id))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_active_transactions(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, b.Title, t.quantity, t.date, t.book_id
        FROM transactions t
        JOIN books b ON t.book_id = b.ID
        WHERE t.status = 'Active' AND t.user_id = ?
    """, (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions


def return_book(transaction_id, book_id, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE transactions SET status = 'Returned' WHERE id = ?", (transaction_id,))
    cursor.execute("UPDATE books SET Available = Available + ? WHERE ID = ?", (quantity, book_id))
    conn.commit()
    conn.close()


init_test_db()