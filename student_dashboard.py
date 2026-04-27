import tkinter as tk
from tkinter import ttk, messagebox
from barcode_generator import BarcodeGenerator
from PIL import Image, ImageTk


class StudentDashboard:
    def __init__(self, root, user_data, db_manager, logout_callback):
        self.root = root
        self.user_data = user_data
        self.db_manager = db_manager
        self.logout_callback = logout_callback
        self.barcode_generator = BarcodeGenerator()

        # Colors
        self.DARK_BG = "#1E1E1E"
        self.PRIMARY_COLOR = "#DC143C"  # Crimson Red
        self.SECONDARY_COLOR = "#2D2D2D"
        self.TEXT_COLOR = "#FFFFFF"

        # Configure root window
        self.root.configure(bg=self.DARK_BG)
        self.root.geometry("900x600")
        self.root.minsize(900, 600)

        self.setup_ui()
        self.load_books()
        self.load_transactions()

        # Start the auto-update loop for transactions
        self.auto_update_transactions()

    def setup_ui(self):
        # Header Frame
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        welcome_lbl = tk.Label(
            header,
            text=f"Welcome, {self.user_data['username']}!",
            bg=self.PRIMARY_COLOR,
            fg=self.TEXT_COLOR,
            font=("Segoe UI", 14, "bold")
        )
        welcome_lbl.pack(side=tk.LEFT, padx=20, pady=15)

        logout_btn = tk.Button(
            header,
            text="Logout",
            bg=self.SECONDARY_COLOR,
            fg=self.TEXT_COLOR,
            relief=tk.FLAT,
            command=self.logout_callback
        )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=15)

        # Style Configuration for Notebook & Treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=self.DARK_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.SECONDARY_COLOR, foreground=self.TEXT_COLOR, padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", self.PRIMARY_COLOR)])

        style.configure("Treeview", background=self.SECONDARY_COLOR, foreground=self.TEXT_COLOR,
                        fieldbackground=self.SECONDARY_COLOR, borderwidth=0)
        style.configure("Treeview.Heading", background=self.PRIMARY_COLOR, foreground=self.TEXT_COLOR, relief=tk.FLAT)
        style.map("Treeview", background=[("selected", self.PRIMARY_COLOR)])

        # Notebook for Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- TAB 1: Library Books ---
        self.books_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(self.books_frame, text="Library Books")

        books_top = tk.Frame(self.books_frame, bg=self.DARK_BG)
        books_top.pack(fill=tk.X, pady=10)

        refresh_btn = tk.Button(
            books_top,
            text="↻ Refresh List",
            bg=self.PRIMARY_COLOR,
            fg=self.TEXT_COLOR,
            relief=tk.FLAT,
            command=self.load_books
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)

        help_lbl = tk.Label(books_top, text="(Double-click a book to view its Barcode)", bg=self.DARK_BG, fg="#AAAAAA")
        help_lbl.pack(side=tk.LEFT, padx=10)

        # Books Treeview
        columns = ('ID', 'Title', 'Author', 'ISBN', 'Available')
        self.books_tree = ttk.Treeview(self.books_frame, columns=columns, show='headings')

        self.books_tree.heading('ID', text='ID')
        self.books_tree.heading('Title', text='Title')
        self.books_tree.heading('Author', text='Author')
        self.books_tree.heading('ISBN', text='ISBN')
        self.books_tree.heading('Available', text='Available')

        self.books_tree.column('ID', width=50, anchor=tk.CENTER)
        self.books_tree.column('Title', width=300)
        self.books_tree.column('Author', width=200)
        self.books_tree.column('ISBN', width=150)
        self.books_tree.column('Available', width=100, anchor=tk.CENTER)

        self.books_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.books_tree.bind('<Double-1>', self.on_book_selected)

        # --- TAB 2: My Transactions ---
        self.trans_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(self.trans_frame, text="My Transactions")

        t_columns = ('Title', 'Borrowed Date', 'Due Date')
        self.trans_tree = ttk.Treeview(self.trans_frame, columns=t_columns, show='headings')

        self.trans_tree.heading('Title', text='Book Title')
        self.trans_tree.heading('Borrowed Date', text='Borrowed Date')
        self.trans_tree.heading('Due Date', text='Due Date')

        self.trans_tree.column('Title', width=400)
        self.trans_tree.column('Borrowed Date', width=200)
        self.trans_tree.column('Due Date', width=200)

        self.trans_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

    def load_books(self):
        # Clear existing
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        # Fetch from DB
        books = self.db_manager.get_all_books()
        for b in books:
            self.books_tree.insert('', tk.END, values=(
                b['book_id'], b['title'], b['author'], b['isbn'], b['available_quantity']
            ))

    def load_transactions(self):
        # Clear existing
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)

        # Fetch currently borrowed books
        borrowed = self.db_manager.get_user_borrowed_books(self.user_data['user_id'])
        for t in borrowed:
            # Slicing up to 16 to remove seconds/microseconds from timestamp
            borrow_date = str(t['transaction_date'])[:16] if t['transaction_date'] else "N/A"
            due_date = str(t['due_date'])[:16] if t['due_date'] else "N/A"

            self.trans_tree.insert('', tk.END, values=(t['title'], borrow_date, due_date))

    def auto_update_transactions(self):
        # Reload the transactions in the background
        self.load_transactions()
        # Schedule this function to run again in 5000 milliseconds (5 seconds)
        self.root.after(5000, self.auto_update_transactions)

    def on_book_selected(self, event):
        selection = self.books_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')

        # Ensure we have the expected number of values
        if len(values) >= 4:
            book_id, title, author, isbn = values[0], values[1], values[2], values[3]
            self.show_barcode(int(book_id), title, author, isbn)

    def show_barcode(self, book_id, title, author, isbn):
        barcode_window = tk.Toplevel(self.root)
        barcode_window.title("Book Info")
        barcode_window.geometry("380x420")
        barcode_window.configure(bg=self.DARK_BG)
        barcode_window.resizable(False, False)

        # Header
        header = tk.Frame(barcode_window, bg=self.PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text="Book Details & Barcode",
            font=("Segoe UI", 12, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.PRIMARY_COLOR
        )
        header_label.pack(pady=10)

        # Content
        content = tk.Frame(barcode_window, bg=self.DARK_BG)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Info card
        info_frame = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        info_frame.pack(fill=tk.X, pady=(0, 12))

        info_items = [
            ("Title:", title[:35]),
            ("Author:", author[:30]),
            ("ISBN:", isbn),
            ("Book ID:", str(book_id))
        ]

        for label_text, value_text in info_items:
            item_frame = tk.Frame(info_frame, bg=self.SECONDARY_COLOR)
            item_frame.pack(fill=tk.X, padx=10, pady=4)

            icon_label = tk.Label(
                item_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                fg=self.PRIMARY_COLOR,
                bg=self.SECONDARY_COLOR,
                width=8,
                anchor="w"
            )
            icon_label.pack(side=tk.LEFT, padx=(0, 5))

            value = tk.Label(
                item_frame,
                text=value_text,
                font=("Segoe UI", 10),
                fg=self.TEXT_COLOR,
                bg=self.SECONDARY_COLOR,
                wraplength=230,
                justify=tk.LEFT
            )
            value.pack(side=tk.LEFT)

        # Barcode section
        barcode_section = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        barcode_section.pack(fill=tk.BOTH, expand=True, pady=8)

        barcode_label = tk.Label(barcode_section, bg=self.SECONDARY_COLOR)
        barcode_label.pack(pady=15)

        try:
            # We use the ISBN for the barcode
            barcode_image = self.barcode_generator.generate_barcode(str(isbn))
            barcode_photo = ImageTk.PhotoImage(barcode_image)

            barcode_label.config(image=barcode_photo)
            barcode_label.image = barcode_photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate barcode: {str(e)}")