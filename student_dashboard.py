import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from qr_generator import QRCodeGenerator
from PIL import Image, ImageTk
import io
from datetime import datetime


class StudentDashboard:

    def __init__(self, root, user_data, db_manager, logout_callback):
        self.root = root
        self.user_data = user_data
        self.db_manager = db_manager
        self.logout_callback = logout_callback

        # Enhanced Color Palette
        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.DARK_BG = "#F8F9FA"
        self.TEXT_COLOR = "#2C3E50"
        self.ACCENT_COLOR = "#E74C3C"
        self.SUCCESS_COLOR = "#27AE60"
        self.INFO_COLOR = "#3498DB"
        self.BORDER_COLOR = "#ECF0F1"
        self.LIGHT_GRAY = "#F5F6FA"
        self.SHADOW_COLOR = "#BDC3C7"

        self.qr_generator = QRCodeGenerator()

        # Configure root window
        self.root.configure(bg=self.DARK_BG)
        self.root.geometry("900x600")
        self.root.minsize(900, 600)

        self.setup_ui()

    def setup_ui(self):
        # Create main container
        main_container = tk.Frame(self.root, bg=self.DARK_BG)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        self._create_header(main_container)

        # Main content area
        content_container = tk.Frame(main_container, bg=self.DARK_BG)
        content_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Right main content (full width, no sidebar)
        right_panel = tk.Frame(content_container, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._create_main_content(right_panel)

    def _create_header(self, parent):
        header = tk.Frame(parent, bg=self.PRIMARY_COLOR, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Header content
        header_content = tk.Frame(header, bg=self.PRIMARY_COLOR)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left side - Welcome message with icon
        left_header = tk.Frame(header_content, bg=self.PRIMARY_COLOR)
        left_header.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        welcome_text = tk.Label(
            left_header,
            text="📚 Library Management",
            font=("Segoe UI", 14, "bold"),
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR
        )
        welcome_text.pack(anchor=tk.W, pady=(2, 0))

        user_info = tk.Label(
            left_header,
            text=f"Welcome, {self.user_data['username']}! 👤 | Student",
            font=("Segoe UI", 9),
            fg="#FFD700",
            bg=self.PRIMARY_COLOR
        )
        user_info.pack(anchor=tk.W, pady=(0, 2))

        # Right side - Logout button
        right_header = tk.Frame(header_content, bg=self.PRIMARY_COLOR)
        right_header.pack(side=tk.RIGHT)

        logout_btn = tk.Button(
            right_header,
            text="🚪 LOGOUT",
            font=("Segoe UI", 9, "bold"),
            bg=self.SECONDARY_COLOR,
            fg=self.PRIMARY_COLOR,
            command=self.logout,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground="#FFE4E1",
            activeforeground=self.PRIMARY_COLOR
        )
        logout_btn.pack()

    def _create_main_content(self, parent):
        # Search Section
        self._create_search_section(parent)

        # Books Display Section
        self._create_books_section(parent)

        # Action Buttons Section
        self._create_action_buttons(parent)

        # Load initial data
        self.load_books()

    def _create_search_section(self, parent):
        search_container = tk.Frame(parent, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=0)
        search_container.pack(fill=tk.X, pady=(0, 12))

        # Rounded effect with padding
        search_frame = tk.Frame(search_container, bg=self.LIGHT_GRAY)
        search_frame.pack(fill=tk.X, padx=0, pady=8)

        search_icon = tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 12),
            fg=self.PRIMARY_COLOR,
            bg=self.LIGHT_GRAY
        )
        search_icon.pack(side=tk.LEFT, padx=(10, 8))

        search_label = tk.Label(
            search_frame,
            text="Search Books:",
            font=("Segoe UI", 9, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.LIGHT_GRAY
        )
        search_label.pack(side=tk.LEFT, padx=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_books())

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 9),
            width=40,
            relief=tk.FLAT,
            bd=0,
            bg=self.SECONDARY_COLOR,
            fg=self.TEXT_COLOR,
            insertbackground=self.PRIMARY_COLOR
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Hover effect
        search_entry.bind("<Enter>", lambda e: search_entry.config(bg="#FFFFFF"))
        search_entry.bind("<Leave>", lambda e: search_entry.config(bg=self.SECONDARY_COLOR))

    def _create_books_section(self, parent):
        """Create books display section with modern styling"""
        books_container = tk.Frame(parent, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        books_container.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        # Title
        title_frame = tk.Frame(books_container, bg=self.SECONDARY_COLOR)
        title_frame.pack(fill=tk.X, padx=0, pady=(8, 8))

        title = tk.Label(
            title_frame,
            text="📖 Available Books",
            font=("Segoe UI", 11, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        )
        title.pack(anchor=tk.W, padx=10)

        # Separator
        separator = tk.Frame(books_container, bg=self.BORDER_COLOR, height=1)
        separator.pack(fill=tk.X, padx=10, pady=(0, 8))

        # Treeview frame
        tree_frame = tk.Frame(books_container, bg=self.SECONDARY_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Treeview",
            background=self.SECONDARY_COLOR,
            foreground=self.TEXT_COLOR,
            rowheight=24,
            fieldbackground=self.SECONDARY_COLOR,
            font=("Segoe UI", 8)
        )
        style.configure(
            "Treeview.Heading",
            background=self.LIGHT_GRAY,
            foreground=self.TEXT_COLOR,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            borderwidth=0
        )
        style.map("Treeview", background=[("selected", self.INFO_COLOR)], foreground=[("selected", "white")])

        # Treeview
        columns = ("ID", "Title", "Author", "ISBN", "Available", "Status")
        self.books_tree = ttk.Treeview(tree_frame, columns=columns, height=8, show="headings", style="Treeview")

        for col in columns:
            self.books_tree.heading(col, text=col)
            if col == "ID":
                self.books_tree.column(col, width=35, anchor="center")
            elif col == "Available":
                self.books_tree.column(col, width=70, anchor="center")
            elif col == "Status":
                self.books_tree.column(col, width=80, anchor="center")
            else:
                self.books_tree.column(col, width=100)

        self.books_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_tree.configure(yscroll=scrollbar.set)

        self.books_tree.bind('<Double-1>', self.on_book_selected)
        self.books_tree.bind('<Button-1>', self.on_tree_select)

    def on_tree_select(self, event):
        pass

    def _create_action_buttons(self, parent):
        button_frame = tk.Frame(parent, bg=self.DARK_BG)
        button_frame.pack(fill=tk.X, pady=(0, 0))

        buttons_container = tk.Frame(button_frame, bg=self.DARK_BG)
        buttons_container.pack(fill=tk.X, pady=10)

        # Borrow button
        borrow_btn = self._create_modern_button(
            buttons_container,
            "📤 BORROW BOOK",
            self.borrow_book,
            self.PRIMARY_COLOR
        )
        borrow_btn.pack(side=tk.LEFT, padx=5)

        # Return button
        return_btn = self._create_modern_button(
            buttons_container,
            "📥 RETURN BOOK",
            self.return_book,
            self.SUCCESS_COLOR
        )
        return_btn.pack(side=tk.LEFT, padx=5)

        # My Books button
        my_books_btn = self._create_modern_button(
            buttons_container,
            "📚 MY BORROWED BOOKS",
            self.show_borrowed_books,
            self.INFO_COLOR
        )
        my_books_btn.pack(side=tk.LEFT, padx=5)

        # Refresh button
        refresh_btn = self._create_modern_button(
            buttons_container,
            "🔄 REFRESH",
            self.refresh_books,
            "#9B59B6"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def _create_modern_button(self, parent, text, command, bg_color):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg=self.SECONDARY_COLOR,
            command=command,
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=10,
            activebackground=bg_color,
            activeforeground=self.SECONDARY_COLOR,
            bd=0
        )
        return btn

    def load_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        try:
            books = self.db_manager.get_all_books()

            for idx, book in enumerate(books):
                status = "Available" if book['available_quantity'] > 0 else "Not Available"
                tag = "available" if book['available_quantity'] > 0 else "unavailable"

                title = book['title'][:30] if len(book['title']) > 30 else book['title']
                author = book['author'][:15] if len(book['author']) > 15 else book['author']

                self.books_tree.insert('', tk.END, values=(
                    book['book_id'],
                    title,
                    author,
                    book['isbn'],
                    book['available_quantity'],
                    status
                ), tags=(tag,))

            # Configure tags
            self.books_tree.tag_configure("available", foreground=self.SUCCESS_COLOR)
            self.books_tree.tag_configure("unavailable", foreground=self.ACCENT_COLOR)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {str(e)}")

    def search_books(self):
        search_term = self.search_var.get()

        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        if not search_term:
            self.load_books()
            return

        try:
            books = self.db_manager.search_books(search_term)

            for book in books:
                status = "Available" if book['available_quantity'] > 0 else "Not Available"
                tag = "available" if book['available_quantity'] > 0 else "unavailable"

                title = book['title'][:30] if len(book['title']) > 30 else book['title']
                author = book['author'][:15] if len(book['author']) > 15 else book['author']

                self.books_tree.insert('', tk.END, values=(
                    book['book_id'],
                    title,
                    author,
                    book['isbn'],
                    book['available_quantity'],
                    status
                ), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search books: {str(e)}")

    def refresh_books(self):
        self.search_var.set("")
        self.load_books()
        messagebox.showinfo("✅ Success", "Books list refreshed successfully!")

    def on_book_selected(self, event):
        selection = self.books_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')
        book_id, title, author, isbn, available, status = values

        self.show_qr_code(int(book_id), title, author, isbn)

    def show_qr_code(self, book_id, title, author, isbn):
        qr_window = tk.Toplevel(self.root)
        qr_window.title("📖 Book Info")
        qr_window.geometry("380x420")
        qr_window.configure(bg=self.DARK_BG)
        qr_window.resizable(False, False)

        # Header
        header = tk.Frame(qr_window, bg=self.PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text="Book Details & QR",
            font=("Segoe UI", 12, "bold"),
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR
        )
        header_label.pack(pady=10)

        # Content
        content = tk.Frame(qr_window, bg=self.DARK_BG)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Info card
        info_frame = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        info_frame.pack(fill=tk.X, pady=(0, 12))

        info_items = [
            ("📚", title[:25]),
            ("✍️", author[:20]),
            ("🔢", isbn),
            ("🆔", str(book_id))
        ]

        for icon, value_text in info_items:
            item_frame = tk.Frame(info_frame, bg=self.SECONDARY_COLOR)
            item_frame.pack(fill=tk.X, padx=10, pady=4)

            icon_label = tk.Label(
                item_frame,
                text=icon,
                font=("Segoe UI", 10),
                fg=self.PRIMARY_COLOR,
                bg=self.SECONDARY_COLOR
            )
            icon_label.pack(side=tk.LEFT, padx=(0, 8))

            value = tk.Label(
                item_frame,
                text=value_text,
                font=("Segoe UI", 9),
                fg=self.TEXT_COLOR,
                bg=self.SECONDARY_COLOR,
                wraplength=300,
                justify=tk.LEFT
            )
            value.pack(side=tk.LEFT)

        # QR Code section
        qr_section = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        qr_section.pack(fill=tk.BOTH, expand=True, pady=8)

        qr_label = tk.Label(qr_section, bg=self.SECONDARY_COLOR)
        qr_label.pack(pady=8)

        try:
            qr_image = self.qr_generator.generate_qr(
                f"ID:{book_id}|Title:{title}|Author:{author}|ISBN:{isbn}"
            )

            qr_image = qr_image.resize((180, 180), Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_image)
            qr_label.config(image=qr_photo)
            qr_label.image = qr_photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

    def borrow_book(self):
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Warning", "Please select a book to borrow")
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')
        book_id, title, author, isbn, available, status = values

        if status == "Not Available":
            messagebox.showerror("❌ Error", "This book is not available")
            return

        try:
            self.db_manager.borrow_book(self.user_data['user_id'], int(book_id))
            messagebox.showinfo("✅ Success", f"Successfully borrowed '{title}'!\n\n📅 Due: 14 days")
            self.load_books()
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))

    def return_book(self):
        """Return selected book"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Warning", "Please select a book to return")
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')
        book_id, title, author, isbn, available, status = values

        try:
            self.db_manager.return_book(self.user_data['user_id'], int(book_id))
            messagebox.showinfo("✅ Success", f"Successfully returned '{title}'!")
            self.load_books()
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))

    def show_borrowed_books(self):
        try:
            borrowed_books = self.db_manager.get_user_borrowed_books(self.user_data['user_id'])

            if not borrowed_books:
                messagebox.showinfo("ℹ️ Info", "You have no borrowed books")
                return

            books_window = tk.Toplevel(self.root)
            books_window.title("My Borrowed Books")
            books_window.geometry("700x350")
            books_window.configure(bg=self.DARK_BG)

            # Header
            header = tk.Frame(books_window, bg=self.PRIMARY_COLOR, height=60)
            header.pack(fill=tk.X)
            header.pack_propagate(False)

            header_content = tk.Frame(header, bg=self.PRIMARY_COLOR)
            header_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

            title_label = tk.Label(
                header_content,
                text="📚 Your Borrowed Books",
                font=("Segoe UI", 12, "bold"),
                fg=self.SECONDARY_COLOR,
                bg=self.PRIMARY_COLOR
            )
            title_label.pack(anchor=tk.W)

            count_label = tk.Label(
                header_content,
                text=f"Total: {len(borrowed_books)} book(s)",
                font=("Segoe UI", 9),
                fg="#FFD700",
                bg=self.PRIMARY_COLOR
            )
            count_label.pack(anchor=tk.W, pady=(3, 0))

            # Content
            content = tk.Frame(books_window, bg=self.DARK_BG)
            content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

            # Configure treeview style
            style = ttk.Style()
            style.configure(
                "Borrowed.Treeview",
                background=self.SECONDARY_COLOR,
                foreground=self.TEXT_COLOR,
                rowheight=26,
                fieldbackground=self.SECONDARY_COLOR,
                font=("Segoe UI", 8)
            )
            style.configure(
                "Borrowed.Treeview.Heading",
                background=self.LIGHT_GRAY,
                foreground=self.TEXT_COLOR,
                font=("Segoe UI", 9, "bold")
            )
            style.map("Borrowed.Treeview", background=[("selected", self.INFO_COLOR)],
                      foreground=[("selected", "white")])

            # Treeview
            columns = ("Title", "Author", "ISBN", "Borrowed", "Due")
            tree = ttk.Treeview(content, columns=columns, height=11, show="headings", style="Borrowed.Treeview")

            for col in columns:
                tree.heading(col, text=col)
                if col in ("Borrowed", "Due"):
                    tree.column(col, width=100)
                else:
                    tree.column(col, width=130)

            for book in borrowed_books:
                title = book['title'][:20] if len(book['title']) > 20 else book['title']
                author = book['author'][:12] if len(book['author']) > 12 else book['author']

                tree.insert('', tk.END, values=(
                    title,
                    author,
                    book['isbn'],
                    book['transaction_date'][:10],
                    book['due_date'][:10]
                ))

            tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

            # Scrollbar
            scrollbar = ttk.Scrollbar(content, orient=tk.VERTICAL, command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscroll=scrollbar.set)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load borrowed books: {str(e)}")

    def logout(self):
        if messagebox.askyesno("🚪 Logout", "Are you sure you want to logout?"):
            self.logout_callback()
