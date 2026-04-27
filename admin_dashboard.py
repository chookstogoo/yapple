import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class AdminDashboard:

    def __init__(self, root, user_data, db_manager, logout_callback):
        self.root = root
        self.user_data = user_data
        self.db_manager = db_manager
        self.logout_callback = logout_callback

        # Colors
        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#333333"
        self.ACCENT_COLOR = "#F5F5F5"

        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg=self.SECONDARY_COLOR)

        # Header
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text=f"👨‍💼 Welcome, {self.user_data['username']}! (Admin)",
            font=("Helvetica", 16, "bold"),
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR
        )
        title.pack(side=tk.LEFT, padx=20, pady=20)

        logout_btn = tk.Button(
            header,
            text="LOGOUT",
            font=("Helvetica", 10, "bold"),
            bg=self.SECONDARY_COLOR,
            fg=self.PRIMARY_COLOR,
            command=self.logout,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=5
        )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=20)

        # Main content with tabs
        content = tk.Frame(self.root, bg=self.SECONDARY_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        notebook = ttk.Notebook(content)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Book Management
        self.book_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.book_tab, text="📚 Book Management")
        self.setup_book_management_tab()

        # Tab 2: Book Status
        self.status_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.status_tab, text="📊 Book Status")
        self.setup_book_status_tab()

        # Tab 3: Transactions
        self.transaction_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.transaction_tab, text="📋 Transactions")
        self.setup_transactions_tab()

    def setup_book_management_tab(self):
        # Button frame
        button_frame = tk.Frame(self.book_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        add_btn = tk.Button(
            button_frame,
            text="➕ ADD NEW BOOK",
            font=("Helvetica", 11, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR,
            command=self.add_book,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(
            button_frame,
            text="🗑️ DELETE BOOK",
            font=("Helvetica", 11, "bold"),
            bg="#DC3545",
            fg=self.SECONDARY_COLOR,
            command=self.delete_book,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        update_btn = tk.Button(
            button_frame,
            text="✏️ UPDATE BOOK",
            font=("Helvetica", 11, "bold"),
            bg="#FFC107",
            fg=self.TEXT_COLOR,
            command=self.update_book,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        update_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(
            button_frame,
            text="🔄 REFRESH",
            font=("Helvetica", 11, "bold"),
            bg="#28A745",
            fg=self.SECONDARY_COLOR,
            command=self.load_books,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Books treeview
        tree_frame = tk.Frame(self.book_tab, bg=self.SECONDARY_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "Title", "Author", "ISBN", "Total Qty", "Available Qty")
        self.books_tree = ttk.Treeview(tree_frame, columns=columns, height=15, show="headings")

        for col in columns:
            self.books_tree.heading(col, text=col)
            if col == "ID":
                self.books_tree.column(col, width=30)
            elif col in ("Total Qty", "Available Qty"):
                self.books_tree.column(col, width=80)
            else:
                self.books_tree.column(col, width=120)

        self.books_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_tree.configure(yscroll=scrollbar.set)

        self.load_books()

    def setup_book_status_tab(self):
        # Status display
        status_frame = tk.Frame(self.status_tab, bg=self.SECONDARY_COLOR)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(status_frame, text="📊 LIBRARY STATISTICS", font=("Helvetica", 14, "bold"),
                fg=self.PRIMARY_COLOR, bg=self.SECONDARY_COLOR).pack(anchor=tk.W, pady=(0, 20))

        # Statistics cards
        stats_container = tk.Frame(status_frame, bg=self.SECONDARY_COLOR)
        stats_container.pack(fill=tk.X, pady=10)

        # Total books
        self.total_books_label = tk.Label(
            stats_container,
            text="Total Books: 0",
            font=("Helvetica", 12, "bold"),
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR,
            padx=20,
            pady=20,
            relief=tk.RAISED,
            bd=2
        )
        self.total_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Available books
        self.available_books_label = tk.Label(
            stats_container,
            text="Available Books: 0",
            font=("Helvetica", 12, "bold"),
            fg=self.SECONDARY_COLOR,
            bg="#28A745",
            padx=20,
            pady=20,
            relief=tk.RAISED,
            bd=2
        )
        self.available_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Borrowed books
        self.borrowed_books_label = tk.Label(
            stats_container,
            text="Borrowed Books: 0",
            font=("Helvetica", 12, "bold"),
            fg=self.SECONDARY_COLOR,
            bg="#007BFF",
            padx=20,
            pady=20,
            relief=tk.RAISED,
            bd=2
        )
        self.borrowed_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Book status treeview
        tk.Label(status_frame, text="\n📖 Individual Book Status:", font=("Helvetica", 12, "bold"),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(anchor=tk.W, pady=(20, 10))

        tree_frame = tk.Frame(status_frame, bg=self.SECONDARY_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Title", "Author", "Total", "Available", "Borrowed")
        self.status_tree = ttk.Treeview(tree_frame, columns=columns, height=12, show="headings")

        for col in columns:
            self.status_tree.heading(col, text=col)
            if col in ("Total", "Available", "Borrowed"):
                self.status_tree.column(col, width=80)
            else:
                self.status_tree.column(col, width=150)

        self.status_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.status_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_tree.configure(yscroll=scrollbar.set)

        refresh_btn = tk.Button(
            status_frame,
            text="🔄 REFRESH STATS",
            font=("Helvetica", 11, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR,
            command=self.load_book_status,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        refresh_btn.pack(pady=(20, 0))

        self.load_book_status()

    def setup_transactions_tab(self):
        # Button frame
        button_frame = tk.Frame(self.transaction_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        refresh_btn = tk.Button(
            button_frame,
            text="🔄 REFRESH TRANSACTIONS",
            font=("Helvetica", 11, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR,
            command=self.load_transactions,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Transactions treeview
        tree_frame = tk.Frame(self.transaction_tab, bg=self.SECONDARY_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "User", "Book Title", "Type", "Date", "Due Date")
        self.transactions_tree = ttk.Treeview(tree_frame, columns=columns, height=15, show="headings")

        for col in columns:
            self.transactions_tree.heading(col, text=col)
            if col == "ID":
                self.transactions_tree.column(col, width=30)
            elif col in ("Type", "Date", "Due Date"):
                self.transactions_tree.column(col, width=90)
            else:
                self.transactions_tree.column(col, width=110)

        self.transactions_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transactions_tree.configure(yscroll=scrollbar.set)

        self.load_transactions()

    def load_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        books = self.db_manager.get_all_books()

        for book in books:
            self.books_tree.insert('', tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['isbn'],
                book['quantity'],
                book['available_quantity']
            ))

    def add_book(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Book")
        add_window.geometry("400x350")
        add_window.configure(bg=self.SECONDARY_COLOR)

        tk.Label(add_window, text="Title:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(20, 5))
        title_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        title_entry.pack(pady=(0, 10))

        tk.Label(add_window, text="Author:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        author_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        author_entry.pack(pady=(0, 10))

        tk.Label(add_window, text="ISBN:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        isbn_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        isbn_entry.pack(pady=(0, 10))

        tk.Label(add_window, text="Quantity:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        quantity_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        quantity_entry.pack(pady=(0, 20))

        def save_book():
            title = title_entry.get()
            author = author_entry.get()
            isbn = isbn_entry.get()
            quantity = quantity_entry.get()

            if not all([title, author, isbn, quantity]):
                messagebox.showerror("Error", "Please fill all fields")
                return

            try:
                quantity = int(quantity)
                self.db_manager.add_book(title, author, isbn, quantity)
                messagebox.showinfo("Success", "Book added successfully!")
                self.load_books()
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn = tk.Button(
            add_window,
            text="SAVE BOOK",
            font=("Helvetica", 11, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR,
            command=save_book,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        save_btn.pack(pady=20)

    def delete_book(self):
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        item = selection[0]
        book_id = self.books_tree.item(item, 'values')[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            try:
                self.db_manager.delete_book(int(book_id))
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.load_books()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_book(self):
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to update")
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')
        book_id, title, author, isbn, total_qty, available_qty = values

        update_window = tk.Toplevel(self.root)
        update_window.title("Update Book")
        update_window.geometry("400x350")
        update_window.configure(bg=self.SECONDARY_COLOR)

        tk.Label(update_window, text="Title:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(20, 5))
        title_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        title_entry.insert(0, title)
        title_entry.pack(pady=(0, 10))

        tk.Label(update_window, text="Author:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        author_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        author_entry.insert(0, author)
        author_entry.pack(pady=(0, 10))

        tk.Label(update_window, text="ISBN:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        isbn_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        isbn_entry.insert(0, isbn)
        isbn_entry.pack(pady=(0, 10))

        tk.Label(update_window, text="Quantity:", font=("Helvetica", 11),
                fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        quantity_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        quantity_entry.insert(0, total_qty)
        quantity_entry.pack(pady=(0, 20))

        def save_update():
            new_title = title_entry.get()
            new_author = author_entry.get()
            new_isbn = isbn_entry.get()
            new_quantity = quantity_entry.get()

            if not all([new_title, new_author, new_isbn, new_quantity]):
                messagebox.showerror("Error", "Please fill all fields")
                return

            try:
                new_quantity = int(new_quantity)
                self.db_manager.update_book(int(book_id), new_title, new_author, new_isbn, new_quantity)
                messagebox.showinfo("Success", "Book updated successfully!")
                self.load_books()
                update_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn = tk.Button(
            update_window,
            text="UPDATE BOOK",
            font=("Helvetica", 11, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR,
            command=save_update,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        save_btn.pack(pady=20)

    def load_book_status(self):
        books = self.db_manager.get_all_books()

        total_qty = sum(book['quantity'] for book in books)
        available_qty = sum(book['available_quantity'] for book in books)
        borrowed_qty = total_qty - available_qty

        # Update labels
        self.total_books_label.config(text=f"Total Books: {total_qty}")
        self.available_books_label.config(text=f"Available Books: {available_qty}")
        self.borrowed_books_label.config(text=f"Borrowed Books: {borrowed_qty}")

        # Clear treeview
        for item in self.status_tree.get_children():
            self.status_tree.delete(item)

        # Add books
        for book in books:
            borrowed = book['quantity'] - book['available_quantity']
            self.status_tree.insert('', tk.END, values=(
                book['title'],
                book['author'],
                book['quantity'],
                book['available_quantity'],
                borrowed
            ))

    def load_transactions(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        transactions = self.db_manager.get_all_transactions()

        for trans in transactions:
            due_date = trans['due_date'] if trans['due_date'] else "N/A"

            self.transactions_tree.insert('', tk.END, values=(
                trans['transaction_id'],
                trans['username'],
                trans['title'],
                trans['transaction_type'].upper(),
                trans['transaction_date'][:10],
                due_date[:10] if due_date != "N/A" else "N/A"
            ))

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()