import sqlite3
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import hashlib

class DatabaseEntity(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def save(self, connection):
        pass


class User(DatabaseEntity):

    def __init__(self, username, password, role, user_id=None):
        self.user_id = user_id
        self.username = username
        self.password = self._hash_password(password)
        self.role = role
        self.created_at = datetime.now()
    
    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at
        }
    
    def save(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password, role, created_at)
                VALUES (?, ?, ?, ?)
            ''', (self.username, self.password, self.role, self.created_at))
            connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise Exception("Username already exists")


class Book(DatabaseEntity):
    
    def __init__(self, title, author, isbn, quantity, book_id=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.available_quantity = quantity
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'quantity': self.quantity,
            'available_quantity': self.available_quantity,
            'created_at': self.created_at
        }
    
    def save(self, connection):
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, isbn, quantity, available_quantity, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.title, self.author, self.isbn, self.quantity, self.available_quantity, self.created_at))
        connection.commit()
        return cursor.lastrowid


class Transaction(DatabaseEntity):
    
    def __init__(self, user_id, book_id, transaction_type, transaction_id=None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.book_id = book_id
        self.transaction_type = transaction_type  # 'borrow' or 'return'
        self.transaction_date = datetime.now()
        self.due_date = datetime.now() + timedelta(days=14) if transaction_type == 'borrow' else None
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'transaction_type': self.transaction_type,
            'transaction_date': self.transaction_date,
            'due_date': self.due_date
        }
    
    def save(self, connection):
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO transactions (user_id, book_id, transaction_type, transaction_date, due_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, self.book_id, self.transaction_type, self.transaction_date, self.due_date))
        connection.commit()
        return cursor.lastrowid


class DatabaseManager:
    
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row

    def create_tables(self):
        cursor = self.connection.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                quantity INTEGER NOT NULL,
                available_quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        ''')
        
        self.connection.commit()
    
    def register_user(self, username, password, role):

        user = User(username, password, role)
        user_id = user.save(self.connection)
        return user_id
    
    def authenticate_user(self, username, password):

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password_hash))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def get_user_by_username(self, username):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def add_book(self, title, author, isbn, quantity):

        book = Book(title, author, isbn, quantity)
        book_id = book.save(self.connection)
        return book_id
    
    def get_all_books(self):

        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM books ORDER BY title ASC')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_book_by_id(self, book_id):

        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
        book = cursor.fetchone()
        return dict(book) if book else None
    
    def search_books(self, search_term):

        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ORDER BY title ASC
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        return [dict(row) for row in cursor.fetchall()]
    
    def borrow_book(self, user_id, book_id):
        cursor = self.connection.cursor()
        
        # Check availability
        cursor.execute('SELECT available_quantity FROM books WHERE book_id = ?', (book_id,))
        result = cursor.fetchone()
        
        if not result or result['available_quantity'] <= 0:
            raise Exception("Book not available")
        
        # Create transaction
        transaction = Transaction(user_id, book_id, 'borrow')
        transaction.save(self.connection)
        
        # Update available quantity
        cursor.execute('''
            UPDATE books SET available_quantity = available_quantity - 1 WHERE book_id = ?
        ''', (book_id,))
        self.connection.commit()
    
    def return_book(self, user_id, book_id):
        cursor = self.connection.cursor()
        
        # Verify user borrowed this book
        cursor.execute('''
            SELECT * FROM transactions 
            WHERE user_id = ? AND book_id = ? AND transaction_type = 'borrow'
            ORDER BY transaction_date DESC LIMIT 1
        ''', (user_id, book_id))
        
        borrow_record = cursor.fetchone()
        if not borrow_record:
            raise Exception("No active borrow record found")
        
        # Create return transaction
        transaction = Transaction(user_id, book_id, 'return')
        transaction.save(self.connection)
        
        # Update available quantity
        cursor.execute('''
            UPDATE books SET available_quantity = available_quantity + 1 WHERE book_id = ?
        ''', (book_id,))
        self.connection.commit()
    
    def get_user_borrowed_books(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT DISTINCT b.*, t.transaction_date, t.due_date
            FROM books b
            JOIN transactions t ON b.book_id = t.book_id
            WHERE t.user_id = ? AND t.transaction_type = 'borrow'
            AND NOT EXISTS (
                SELECT 1 FROM transactions t2 
                WHERE t2.user_id = ? AND t2.book_id = b.book_id 
                AND t2.transaction_type = 'return'
                AND t2.transaction_date > t.transaction_date
            )
        ''', (user_id, user_id))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_transactions(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT t.*, u.username, b.title 
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN books b ON t.book_id = b.book_id
            ORDER BY t.transaction_date DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_book(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
        self.connection.commit()
    
    def update_book(self, book_id, title, author, isbn, quantity):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE books 
            SET title = ?, author = ?, isbn = ?, quantity = ?
            WHERE book_id = ?
        ''', (title, author, isbn, quantity, book_id))
        self.connection.commit()