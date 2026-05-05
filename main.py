import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Import your non-UI logic and external scanner/generator tools
from database import DatabaseManager
from barcode_scanner import BarcodeScannerWindow
from barcode_generator import BarcodeGenerator


class LoginWindow:
    def __init__(self, root, on_login_callback, db_manager):
        self.root = root
        self.on_login_callback = on_login_callback
        self.db_manager = db_manager

        # Colors
        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#333333"
        self.LIGHT_GRAY = "#F5F5F5"
        self.ACCENT_GRAY = "#999999"
        self.BORDER_COLOR = "#E0E0E0"
        self.current_mode = "login"

        try:
            self.original_image = Image.open("image (37).png")
        except FileNotFoundError:
            self.original_image = None
            print("Warning: image (37).png not found in the finaleproject folder.")

        self.setup_ui()

    def resize_image(self, event):
        if not self.original_image: return
        new_width, new_height = event.width, event.height
        if new_width > 10 and new_height > 10:
            img_ratio = self.original_image.width / self.original_image.height
            canvas_ratio = new_width / new_height
            if canvas_ratio > img_ratio:
                calc_height = new_height
                calc_width = int(calc_height * img_ratio)
            else:
                calc_width = new_width
                calc_height = int(calc_width / img_ratio)
            resized = self.original_image.resize((calc_width, calc_height), Image.Resampling.LANCZOS)
            self.display_image = ImageTk.PhotoImage(resized)
            self.image_canvas.delete("all")
            self.image_canvas.create_image(new_width // 2, new_height // 2, anchor=tk.CENTER,
                                           image=self.display_image)

    def setup_ui(self):
        for widget in self.root.winfo_children(): widget.destroy()
        self.root.configure(bg=self.SECONDARY_COLOR)

        main_container = tk.Frame(self.root, bg=self.SECONDARY_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)

        left_sidebar = tk.Frame(main_container, bg=self.PRIMARY_COLOR, width=400)
        left_sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_sidebar.pack_propagate(False)

        sidebar_content = tk.Frame(left_sidebar, bg=self.PRIMARY_COLOR)
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=40)

        title_frame = tk.Frame(sidebar_content, bg=self.PRIMARY_COLOR)
        title_frame.pack(pady=(0, 40))
        tk.Label(title_frame, text="📚", font=("Helvetica", 60), bg=self.PRIMARY_COLOR,
                 fg=self.SECONDARY_COLOR).pack()
        tk.Label(title_frame, text="LIBRARY", font=("Helvetica", 32, "bold"), bg=self.PRIMARY_COLOR,
                 fg=self.SECONDARY_COLOR).pack()
        tk.Label(title_frame, text="MANAGEMENT SYSTEM", font=("Helvetica", 12), bg=self.PRIMARY_COLOR,
                 fg=self.SECONDARY_COLOR).pack()

        tk.Label(sidebar_content, text="━" * 30, font=("Helvetica", 10), bg=self.PRIMARY_COLOR,
                 fg=self.SECONDARY_COLOR).pack(pady=20)

        features = ["Manage Books", "Manage Users", "Manage Knowledge"]
        for feature_text in features:
            feature_frame = tk.Frame(sidebar_content, bg=self.PRIMARY_COLOR)
            feature_frame.pack(pady=15, anchor=tk.W)
            tk.Label(feature_frame, text=f"● {feature_text}", font=("Helvetica", 13), bg=self.PRIMARY_COLOR,
                     fg=self.SECONDARY_COLOR).pack()

        self.image_canvas = tk.Canvas(sidebar_content, bg=self.PRIMARY_COLOR, highlightthickness=0)
        self.image_canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(20, 0))
        self.image_canvas.bind("<Configure>", self.resize_image)

        right_section = tk.Frame(main_container, bg=self.SECONDARY_COLOR)
        right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        outer_frame = tk.Frame(right_section, bg=self.SECONDARY_COLOR)
        outer_frame.pack(fill=tk.BOTH, expand=True)

        self.center_container = tk.Frame(outer_frame, bg=self.SECONDARY_COLOR)
        self.center_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380)

        toggle_frame = tk.Frame(self.center_container, bg=self.SECONDARY_COLOR)
        toggle_frame.pack(fill=tk.X, pady=(0, 30))

        self.login_toggle_btn = tk.Button(toggle_frame, text="Log In", font=("Helvetica", 16, "bold"),
                                          bg=self.SECONDARY_COLOR, fg=self.PRIMARY_COLOR,
                                          command=self.show_login_form,
                                          relief=tk.FLAT, cursor="hand2", padx=30, pady=10, bd=0)
        self.login_toggle_btn.pack(side=tk.LEFT, padx=0)

        tk.Label(toggle_frame, text=" | ", font=("Helvetica", 16), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.signup_toggle_btn = tk.Button(toggle_frame, text="Sign Up", font=("Helvetica", 16),
                                           bg=self.SECONDARY_COLOR, fg=self.ACCENT_GRAY,
                                           command=self.show_signup_form,
                                           relief=tk.FLAT, cursor="hand2", padx=30, pady=10, bd=0)
        self.signup_toggle_btn.pack(side=tk.LEFT, padx=0)

        self.toggle_underline = tk.Frame(self.center_container, bg=self.PRIMARY_COLOR, height=3)
        self.toggle_underline.pack(fill=tk.X, pady=(0, 20))

        self.content_frame = tk.Frame(self.center_container, bg=self.SECONDARY_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=False)

        self.show_login_form()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children(): widget.destroy()

    def show_login_form(self):
        self.current_mode = "login"
        self.clear_content_frame()
        self.login_toggle_btn.configure(fg=self.PRIMARY_COLOR, font=("Helvetica", 16, "bold"))
        self.signup_toggle_btn.configure(fg=self.ACCENT_GRAY, font=("Helvetica", 16))

        tk.Label(self.content_frame, text="Welcome Back!", font=("Helvetica", 20, "bold"),
                 fg=self.PRIMARY_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(0, 5))
        tk.Label(self.content_frame, text="Please log in to your account", font=("Helvetica", 10),
                 fg=self.ACCENT_GRAY, bg=self.SECONDARY_COLOR).pack(pady=(0, 25))

        username_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(username_frame, text="👤", font=("Helvetica", 12), bg=self.LIGHT_GRAY,
                 fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)
        self.login_username = tk.Entry(username_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY,
                                       border=0, fg=self.TEXT_COLOR)
        self.login_username.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

        password_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        password_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(password_frame, text="🔒", font=("Helvetica", 12), bg=self.LIGHT_GRAY,
                 fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)
        self.login_password = tk.Entry(password_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY,
                                       border=0, fg=self.TEXT_COLOR, show="*")
        self.login_password.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

        role_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        role_frame.pack(fill=tk.X, pady=(0, 25))
        tk.Label(role_frame, text="🛡️", font=("Helvetica", 12), bg=self.LIGHT_GRAY,
                 fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)
        self.login_role = ttk.Combobox(role_frame, values=["Student", "Admin"], state="readonly",
                                        font=("Helvetica", 11), width=25)
        self.login_role.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 10))
        self.login_role.set("Student")

        login_submit_btn = tk.Button(self.content_frame, text="Log In", font=("Helvetica", 12, "bold"),
                                     bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR,
                                     command=self.perform_login,
                                     relief=tk.FLAT, cursor="hand2", padx=20, pady=12)
        login_submit_btn.pack(fill=tk.X, pady=(0, 15))

    def show_signup_form(self):
        self.current_mode = "signup"
        self.clear_content_frame()
        self.login_toggle_btn.configure(fg=self.ACCENT_GRAY, font=("Helvetica", 16))
        self.signup_toggle_btn.configure(fg=self.PRIMARY_COLOR, font=("Helvetica", 16, "bold"))

        tk.Label(self.content_frame, text="Create Account", font=("Helvetica", 20, "bold"),
                 fg=self.PRIMARY_COLOR, bg=self.SECONDARY_COLOR).pack(pady=(0, 5))

        username_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(username_frame, text="👤", font=("Helvetica", 12), bg=self.LIGHT_GRAY,
                 fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)
        self.signup_username = tk.Entry(username_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY,
                                        border=0, fg=self.TEXT_COLOR)
        self.signup_username.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

        password_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        password_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(password_frame, text="🔒", font=("Helvetica", 12), bg=self.LIGHT_GRAY,
                 fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)
        self.signup_password = tk.Entry(password_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY,
                                        border=0, fg=self.TEXT_COLOR, show="*")
        self.signup_password.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

        role_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        role_frame.pack(fill=tk.X, pady=(0, 25))
        tk.Label(role_frame, text="🛡️", font=("Helvetica", 12), bg=self.LIGHT_GRAY,
                 fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)
        self.signup_role = ttk.Combobox(role_frame, values=["Student", "Admin"], state="readonly",
                                         font=("Helvetica", 11), width=25)
        self.signup_role.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 10))
        self.signup_role.set("Student")

        signup_submit_btn = tk.Button(self.content_frame, text="Sign Up", font=("Helvetica", 12, "bold"),
                                      bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR,
                                      command=self.perform_signup,
                                      relief=tk.FLAT, cursor="hand2", padx=20, pady=12)
        signup_submit_btn.pack(fill=tk.X, pady=(0, 15))

    def perform_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        role = self.login_role.get()
        user = self.db_manager.authenticate_user(username, password)
        if not user or user['role'] != role:
            messagebox.showerror("Error", "Invalid username, password, or role")
            return
        self.on_login_callback(user)

    def perform_signup(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()
        role = self.signup_role.get()
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        try:
            self.db_manager.register_user(username, password, role)
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.show_login_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class AdminDashboard:
    def __init__(self, root, user_data, db_manager, logout_callback):
        self.root = root
        self.user_data = user_data
        self.db_manager = db_manager
        self.logout_callback = logout_callback

        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#333333"
        self.ACCENT_COLOR = "#F5F5F5"

        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg=self.SECONDARY_COLOR)

        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text=f"👨‍💼 Welcome, {self.user_data['username']}! (Admin)",
                         font=("Helvetica", 16, "bold"), fg=self.SECONDARY_COLOR, bg=self.PRIMARY_COLOR)
        title.pack(side=tk.LEFT, padx=20, pady=20)

        logout_btn = tk.Button(header, text="LOGOUT", font=("Helvetica", 10, "bold"),
                               bg=self.SECONDARY_COLOR, fg=self.PRIMARY_COLOR,
                               command=self.logout, relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=20)

        content = tk.Frame(self.root, bg=self.SECONDARY_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        notebook = ttk.Notebook(content)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.book_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.book_tab, text="📚 Book Management")
        self.setup_book_management_tab()

        self.status_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.status_tab, text="📊 Book Status")
        self.setup_book_status_tab()

        self.transaction_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.transaction_tab, text="📋 Transactions")
        self.setup_transactions_tab()

        self.pending_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.pending_tab, text="⏳ Pending Requests")
        self.setup_pending_tab()

    def setup_book_management_tab(self):
        button_frame = tk.Frame(self.book_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(button_frame, text="➕ ADD NEW BOOK", font=("Helvetica", 11, "bold"),
                  bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR, command=self.add_book,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗑️ DELETE BOOK", font=("Helvetica", 11, "bold"),
                  bg="#DC3545", fg=self.SECONDARY_COLOR, command=self.delete_book,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="✏️ UPDATE BOOK", font=("Helvetica", 11, "bold"),
                  bg="#FFC107", fg=self.TEXT_COLOR, command=self.update_book,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔄 REFRESH", font=("Helvetica", 11, "bold"),
                  bg="#28A745", fg=self.SECONDARY_COLOR, command=self.load_books,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📷 SCAN BOOK", font=("Helvetica", 11, "bold"),
                  bg="#17A2B8", fg=self.SECONDARY_COLOR, command=self.open_scanner,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)

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

    def open_scanner(self):
        BarcodeScannerWindow(self.root, self.handle_scanned_barcode)

    def _digits_only(self, s):
        return "".join(c for c in str(s) if c.isdigit())

    def handle_scanned_barcode(self, scanned_isbn):
        if scanned_isbn == "X" or not scanned_isbn:
            self.root.after(100, lambda: messagebox.showerror("Scan Error",
                                                               "The scanner couldn't read the barcode clearly."))
            return
        scan_key = self._digits_only(scanned_isbn)
        found = False
        for item in self.books_tree.get_children():
            values = self.books_tree.item(item, 'values')
            if len(values) >= 4 and self._digits_only(values[3]) == scan_key:
                self.books_tree.selection_set(item)
                self.books_tree.focus(item)
                self.books_tree.see(item)
                found = True
                book_title = values[1]
                self.root.after(100, lambda t=book_title: messagebox.showinfo("Scanner Success",
                                                                                f"Found book: {t}"))
                break
        if not found:
            def ask_to_add():
                if messagebox.askyesno("New Book Detected",
                                        f"Scanned ISBN: {scanned_isbn}\n\nAdd this book now?"):
                    self.add_book(prefill_isbn=scanned_isbn)
            self.root.after(100, ask_to_add)

    def setup_book_status_tab(self):
        status_frame = tk.Frame(self.status_tab, bg=self.SECONDARY_COLOR)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(status_frame, text="📊 LIBRARY STATISTICS", font=("Helvetica", 14, "bold"),
                 fg=self.PRIMARY_COLOR, bg=self.SECONDARY_COLOR).pack(anchor=tk.W, pady=(0, 20))

        stats_container = tk.Frame(status_frame, bg=self.SECONDARY_COLOR)
        stats_container.pack(fill=tk.X, pady=10)

        self.total_books_label = tk.Label(stats_container, text="Total Books: 0",
                                           font=("Helvetica", 12, "bold"), fg=self.SECONDARY_COLOR,
                                           bg=self.PRIMARY_COLOR, padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.total_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.available_books_label = tk.Label(stats_container, text="Available Books: 0",
                                               font=("Helvetica", 12, "bold"), fg=self.SECONDARY_COLOR,
                                               bg="#28A745", padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.available_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.borrowed_books_label = tk.Label(stats_container, text="Borrowed Books: 0",
                                              font=("Helvetica", 12, "bold"), fg=self.SECONDARY_COLOR,
                                              bg="#007BFF", padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.borrowed_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

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

        tk.Button(status_frame, text="🔄 REFRESH STATS", font=("Helvetica", 11, "bold"),
                  bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR, command=self.load_book_status,
                  relief=tk.FLAT, padx=15, pady=8).pack(pady=(20, 0))

        self.load_book_status()

    def setup_transactions_tab(self):
        button_frame = tk.Frame(self.transaction_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(button_frame, text="🔄 REFRESH TRANSACTIONS", font=("Helvetica", 11, "bold"),
                  bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR, command=self.load_transactions,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)

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

    def setup_pending_tab(self):
        btn_frame = tk.Frame(self.pending_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        btn_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(btn_frame, text="✅ APPROVE SELECTED", font=("Helvetica", 11, "bold"),
                  bg="#28A745", fg=self.SECONDARY_COLOR, command=self.approve_request,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 REFRESH", font=("Helvetica", 11, "bold"),
                  bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR, command=self.load_pending,
                  relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.pending_tab, bg=self.SECONDARY_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Columns must match what get_pending_requests() now returns
        cols = ("Trans ID", "User", "Book Title", "Qty Requested", "Date Requested")
        self.pending_tree = ttk.Treeview(tree_frame, columns=cols, height=15, show="headings")
        for col in cols:
            self.pending_tree.heading(col, text=col)
            if col == "Trans ID":
                self.pending_tree.column(col, width=60)
            elif col == "Qty Requested":
                self.pending_tree.column(col, width=100)
            elif col == "Date Requested":
                self.pending_tree.column(col, width=150)
            else:
                self.pending_tree.column(col, width=180)
        self.pending_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.pending_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pending_tree.configure(yscroll=scrollbar.set)

        self.load_pending()

    def load_books(self):
        for item in self.books_tree.get_children(): self.books_tree.delete(item)
        for book in self.db_manager.get_all_books():
            self.books_tree.insert('', tk.END, values=(
                book['book_id'], book['title'], book['author'],
                book['isbn'], book['quantity'], book['available_quantity']
            ))

    def add_book(self, prefill_isbn=""):
        pass  # Keep your standard modal logic here
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Book")
        add_window.geometry("400x350")
        add_window.configure(bg=self.SECONDARY_COLOR)
        add_window.transient(self.root)
        add_window.lift()
        add_window.focus_force()

        tk.Label(add_window, text="Title:", font=("Helvetica", 11), fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(
            pady=(20, 5))
        title_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        title_entry.pack(pady=(0, 10))

        tk.Label(add_window, text="Author:", font=("Helvetica", 11), fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(
            pady=(10, 5))
        author_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        author_entry.pack(pady=(0, 10))

        tk.Label(add_window, text="ISBN:", font=("Helvetica", 11), fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(
            pady=(10, 5))
        isbn_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        if prefill_isbn:
            isbn_entry.insert(0, prefill_isbn)
        isbn_entry.pack(pady=(0, 10))

        tk.Label(add_window, text="Quantity:", font=("Helvetica", 11), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        quantity_entry = tk.Entry(add_window, font=("Helvetica", 10), width=40)
        quantity_entry.pack(pady=(0, 20))

        def save_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            isbn = isbn_entry.get().strip()
            quantity = quantity_entry.get().strip()

            if not all([title, author, isbn, quantity]):
                messagebox.showerror("Error", "Please fill all fields")
                return

            try:
                quantity = int(quantity)
                self.db_manager.add_book(title, author, isbn, quantity)
                messagebox.showinfo("Success", "Book added successfully!")
                self.load_books()
                self.load_book_status()
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_window, text="SAVE BOOK", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=save_book, relief=tk.FLAT, cursor="hand2", padx=20,
                  pady=10).pack(pady=20)

    def delete_book(self):
        pass
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
                self.load_book_status()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_book(self):
        pass
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
        update_window.transient(self.root)
        update_window.lift()
        update_window.focus_force()

        tk.Label(update_window, text="Title:", font=("Helvetica", 11), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(pady=(20, 5))
        title_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        title_entry.insert(0, title)
        title_entry.pack(pady=(0, 10))

        tk.Label(update_window, text="Author:", font=("Helvetica", 11), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        author_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        author_entry.insert(0, author)
        author_entry.pack(pady=(0, 10))

        tk.Label(update_window, text="ISBN:", font=("Helvetica", 11), fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(
            pady=(10, 5))
        isbn_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        isbn_entry.insert(0, isbn)
        isbn_entry.pack(pady=(0, 10))

        tk.Label(update_window, text="Quantity:", font=("Helvetica", 11), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(pady=(10, 5))
        quantity_entry = tk.Entry(update_window, font=("Helvetica", 10), width=40)
        quantity_entry.insert(0, total_qty)
        quantity_entry.pack(pady=(0, 20))

        def save_update():
            new_title = title_entry.get().strip()
            new_author = author_entry.get().strip()
            new_isbn = isbn_entry.get().strip()
            new_quantity = quantity_entry.get().strip()

            if not all([new_title, new_author, new_isbn, new_quantity]):
                messagebox.showerror("Error", "Please fill all fields")
                return

            try:
                new_quantity = int(new_quantity)
                self.db_manager.update_book(int(book_id), new_title, new_author, new_isbn, new_quantity)
                messagebox.showinfo("Success", "Book updated successfully!")
                self.load_books()
                self.load_book_status()
                update_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(update_window, text="UPDATE BOOK", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=save_update, relief=tk.FLAT, cursor="hand2", padx=20,
                  pady=10).pack(pady=20)

    def load_book_status(self):
        books = self.db_manager.get_all_books()
        total_qty = sum(book['quantity'] for book in books)
        available_qty = sum(book['available_quantity'] for book in books)
        self.total_books_label.config(text=f"Total Books: {total_qty}")
        self.available_books_label.config(text=f"Available Books: {available_qty}")
        self.borrowed_books_label.config(text=f"Borrowed Books: {total_qty - available_qty}")
        for item in self.status_tree.get_children(): self.status_tree.delete(item)
        for book in books:
            self.status_tree.insert('', tk.END, values=(
                book['title'], book['author'], book['quantity'],
                book['available_quantity'], book['quantity'] - book['available_quantity']
            ))

    def load_transactions(self):
        for item in self.transactions_tree.get_children(): self.transactions_tree.delete(item)
        for trans in self.db_manager.get_all_transactions():
            self.transactions_tree.insert('', tk.END, values=(
                trans['transaction_id'], trans['username'], trans['title'],
                trans['transaction_type'].upper(), trans['transaction_date'][:10],
                trans['due_date'][:10] if trans['due_date'] else "N/A"
            ))

    def load_pending(self):
        """Load pending requests using the corrected keys from get_pending_requests()."""
        for item in self.pending_tree.get_children(): self.pending_tree.delete(item)
        for r in self.db_manager.get_pending_requests():
            date_str = str(r['transaction_date'])[:16] if r['transaction_date'] else "N/A"
            self.pending_tree.insert('', tk.END, values=(
                r['transaction_id'],
                r['username'],
                r['title'],
                r['qty_requested'],
                date_str
            ))

    def approve_request(self):
        selection = self.pending_tree.selection()
        if not selection:
            return messagebox.showwarning("Warning", "Select a pending request to approve.")

        # Get the transaction_id from the selected row
        trans_id = self.pending_tree.item(selection[0], 'values')[0]

        # Find the full request record by matching transaction_id
        reqs = self.db_manager.get_pending_requests()
        req = next((r for r in reqs if str(r['transaction_id']) == str(trans_id)), None)

        if req:
            self.db_manager.admin_approve_request(
                req['transaction_id'],
                req['user_id'],
                req['book_id'],
                req['qty_requested']
            )
            messagebox.showinfo("Success", f"Request for '{req['title']}' approved!")
            self.load_pending()
            self.load_books()
            self.load_book_status()
        else:
            messagebox.showerror("Error", "Could not find the selected request. Please refresh.")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()


class StudentDashboard:
    def __init__(self, root, user_data, db_manager, logout_callback):
        self.root = root
        self.user_data = user_data
        self.db_manager = db_manager
        self.logout_callback = logout_callback
        self.barcode_generator = BarcodeGenerator()
        self.cart = []

        # ----- Light Mode Colors (dark mode removed) -----
        self.BG_COLOR = "#FFFFFF"
        self.CARD_COLOR = "#F5F5F5"
        self.PRIMARY_COLOR = "#DC143C"
        self.TEXT_COLOR = "#333333"
        self.SUBTEXT_COLOR = "#666666"
        # --------------------------------------------------

        self.root.configure(bg=self.BG_COLOR)
        self.root.geometry("900x700")
        self.setup_ui()
        self.load_books()
        self.load_transactions()
        self.auto_update_transactions()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text=f"Welcome, {self.user_data['username']}!",
                 bg=self.PRIMARY_COLOR, fg="#FFFFFF",
                 font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=20, pady=15)

        tk.Button(header, text="Logout", bg="#FFFFFF", fg=self.PRIMARY_COLOR,
                  relief=tk.FLAT, command=self.logout_callback,
                  font=("Segoe UI", 10, "bold")).pack(side=tk.RIGHT, padx=20, pady=15)

        # Light ttk styles
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=self.BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.CARD_COLOR,
                        foreground=self.TEXT_COLOR, padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", self.PRIMARY_COLOR)],
                  foreground=[("selected", "#FFFFFF")])
        style.configure("Treeview", background="#FFFFFF", foreground=self.TEXT_COLOR,
                        fieldbackground="#FFFFFF", borderwidth=1)
        style.configure("Treeview.Heading", background=self.PRIMARY_COLOR,
                        foreground="#FFFFFF", relief=tk.FLAT, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", self.PRIMARY_COLOR)],
                  foreground=[("selected", "#FFFFFF")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- TAB 1: Library Books ---
        self.books_frame = tk.Frame(self.notebook, bg=self.BG_COLOR)
        self.notebook.add(self.books_frame, text="Library Books")

        books_top = tk.Frame(self.books_frame, bg=self.BG_COLOR)
        books_top.pack(fill=tk.X, pady=10)

        tk.Button(books_top, text="↻ Refresh List", bg=self.PRIMARY_COLOR, fg="#FFFFFF",
                  relief=tk.FLAT, command=self.load_books,
                  font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=10)
        tk.Label(books_top, text="(Double-click a book to view its Barcode)",
                 bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR).pack(side=tk.LEFT, padx=10)

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
        self.books_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.books_tree.bind('<Double-1>', self.on_book_selected)

        # Request Book Cart Section
        req_frame = tk.Frame(self.books_frame, bg=self.CARD_COLOR, pady=10,
                             relief=tk.GROOVE, bd=1)
        req_frame.pack(fill=tk.X, padx=10, pady=10)

        top_req = tk.Frame(req_frame, bg=self.CARD_COLOR)
        top_req.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(top_req, text="Request Book:", bg=self.CARD_COLOR, fg=self.TEXT_COLOR,
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.req_combo = ttk.Combobox(top_req, state="readonly", width=40)
        self.req_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(top_req, text="Qty:", bg=self.CARD_COLOR, fg=self.TEXT_COLOR,
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.req_qty = tk.Entry(top_req, width=5, bg="#FFFFFF", fg=self.TEXT_COLOR)
        self.req_qty.insert(0, "1")
        self.req_qty.pack(side=tk.LEFT, padx=5)

        tk.Button(top_req, text="Add to Cart", bg=self.PRIMARY_COLOR, fg="#FFFFFF",
                  relief=tk.FLAT, command=self.add_to_cart,
                  font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=10)

        bot_req = tk.Frame(req_frame, bg=self.CARD_COLOR)
        bot_req.pack(fill=tk.X, padx=10, pady=5)

        self.cart_text = tk.Text(bot_req, height=3, width=50, bg="#FFFFFF", fg=self.TEXT_COLOR,
                                  relief=tk.GROOVE, bd=1)
        self.cart_text.pack(side=tk.LEFT, padx=5)

        tk.Button(bot_req, text="Submit Request to Admin", bg="#28A745", fg="#FFFFFF",
                  relief=tk.FLAT, font=("Segoe UI", 10, "bold"),
                  command=self.submit_request).pack(side=tk.LEFT, padx=20, fill=tk.Y)

        # --- TAB 2: My Transactions ---
        self.trans_frame = tk.Frame(self.notebook, bg=self.BG_COLOR)
        self.notebook.add(self.trans_frame, text="My Transactions")

        # Added "Status" column so students can see Pending vs Active borrows
        t_columns = ('Trans ID', 'Title', 'Status', 'Borrowed Date', 'Due Date')
        self.trans_tree = ttk.Treeview(self.trans_frame, columns=t_columns, show='headings')
        self.trans_tree.heading('Trans ID', text='ID')
        self.trans_tree.heading('Title', text='Book Title')
        self.trans_tree.heading('Status', text='Status')
        self.trans_tree.heading('Borrowed Date', text='Date')
        self.trans_tree.heading('Due Date', text='Due Date')
        self.trans_tree.column('Trans ID', width=50, anchor=tk.CENTER)
        self.trans_tree.column('Title', width=300)
        self.trans_tree.column('Status', width=100, anchor=tk.CENTER)
        self.trans_tree.column('Borrowed Date', width=160)
        self.trans_tree.column('Due Date', width=160)
        self.trans_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(20, 5))

        # Return section
        ret_frame = tk.Frame(self.trans_frame, bg=self.BG_COLOR)
        ret_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(ret_frame,
                 text="Note: Only 'Active' (approved) books can be returned.",
                 bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR,
                 font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=10)

        tk.Button(ret_frame, text="Return Selected Book", bg="#28A745", fg="#FFFFFF",
                  relief=tk.FLAT, font=("Segoe UI", 11, "bold"),
                  command=self.process_return).pack(side=tk.RIGHT, padx=10)

    def load_books(self):
        for item in self.books_tree.get_children(): self.books_tree.delete(item)
        self.avail_books = self.db_manager.get_all_books()
        for b in self.avail_books:
            self.books_tree.insert('', tk.END, values=(
                b['book_id'], b['title'], b['author'], b['isbn'], b['available_quantity']
            ))
        self.req_combo['values'] = [
            f"[{b['book_id']}] {b['title']} (Avail: {b['available_quantity']})"
            for b in self.avail_books
        ]

    def add_to_cart(self):
        sel = self.req_combo.get()
        qty = self.req_qty.get()
        if not sel or not qty.isdigit() or int(qty) <= 0:
            messagebox.showwarning("Warning", "Please select a book and enter a valid quantity.")
            return
        book_id = int(sel.split(']')[0].replace('[', ''))
        title = sel.split('] ')[1].split(' (Avail:')[0]
        self.cart.append({'book_id': book_id, 'title': title, 'qty': int(qty)})
        self.cart_text.insert(tk.END, f"{title} (Qty: {qty})\n")
        self.req_qty.delete(0, tk.END)
        self.req_qty.insert(0, "1")

    def submit_request(self):
        """Submit all cart items as pending requests to admin."""
        if not self.cart:
            messagebox.showwarning("Warning", "Your cart is empty. Add at least one book.")
            return
        self.db_manager.request_books(self.user_data['user_id'], self.cart)
        self.cart.clear()
        self.cart_text.delete(1.0, tk.END)
        messagebox.showinfo("Success", "Request sent! Check 'My Transactions' — status is Pending Admin Approval.")
        self.load_transactions()

    def load_transactions(self):
        """Load all active/pending transactions and display them with a Status column."""
        for item in self.trans_tree.get_children(): self.trans_tree.delete(item)
        self.borrowed = self.db_manager.get_user_borrowed_books(self.user_data['user_id'])
        for t in self.borrowed:
            status = str(t.get('status', 'N/A'))
            date_str = str(t['transaction_date'])[:16] if t['transaction_date'] else "N/A"
            due_str = str(t['due_date'])[:16] if t.get('due_date') else "Pending Approval"
            self.trans_tree.insert('', tk.END, values=(
                t['transaction_id'], t['title'], status, date_str, due_str
            ))

    def process_return(self):
        selected = self.trans_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book from the list to return.")
            return

        values = self.trans_tree.item(selected[0], 'values')
        trans_id = values[0]
        status = values[2]

        if status != 'Active':
            messagebox.showwarning("Warning",
                                   "Only 'Active' (approved) books can be returned.\n"
                                   "Pending requests cannot be returned.")
            return

        t = next((x for x in self.borrowed if str(x['transaction_id']) == str(trans_id)), None)
        if t:
            self.db_manager.return_book(t['transaction_id'], t['book_id'], t['transaction_type'])
            messagebox.showinfo("Success", "Book returned successfully!")
            self.load_transactions()
            self.load_books()

    def auto_update_transactions(self):
        self.load_transactions()
        self.root.after(5000, self.auto_update_transactions)

    def on_book_selected(self, event):
        selection = self.books_tree.selection()
        if not selection: return
        values = self.books_tree.item(selection[0], 'values')
        if len(values) >= 4:
            self.show_barcode(int(values[0]), values[1], values[2], values[3])

    def show_barcode(self, book_id, title, author, isbn):
        barcode_window = tk.Toplevel(self.root)
        barcode_window.title("Book Info")
        barcode_window.geometry("380x420")
        barcode_window.configure(bg=self.BG_COLOR)
        barcode_window.resizable(False, False)

        header = tk.Frame(barcode_window, bg=self.PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Book Details & Barcode", font=("Segoe UI", 12, "bold"),
                 fg="#FFFFFF", bg=self.PRIMARY_COLOR).pack(pady=10)

        content = tk.Frame(barcode_window, bg=self.BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        info_frame = tk.Frame(content, bg=self.CARD_COLOR, relief=tk.GROOVE, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 12))

        for label_text, value_text in [("Title:", title[:35]), ("Author:", author[:30]),
                                        ("ISBN:", isbn), ("Book ID:", str(book_id))]:
            item_frame = tk.Frame(info_frame, bg=self.CARD_COLOR)
            item_frame.pack(fill=tk.X, padx=10, pady=4)
            tk.Label(item_frame, text=label_text, font=("Segoe UI", 10, "bold"),
                     fg=self.PRIMARY_COLOR, bg=self.CARD_COLOR, width=8, anchor="w").pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(item_frame, text=value_text, font=("Segoe UI", 10),
                     fg=self.TEXT_COLOR, bg=self.CARD_COLOR,
                     wraplength=230, justify=tk.LEFT).pack(side=tk.LEFT)

        barcode_section = tk.Frame(content, bg=self.CARD_COLOR, relief=tk.GROOVE, bd=1)
        barcode_section.pack(fill=tk.BOTH, expand=True, pady=8)

        barcode_label = tk.Label(barcode_section, bg=self.CARD_COLOR)
        barcode_label.pack(pady=15)

        try:
            barcode_image = self.barcode_generator.generate_barcode(str(isbn))
            barcode_photo = ImageTk.PhotoImage(barcode_image)
            barcode_label.config(image=barcode_photo)
            barcode_label.image = barcode_photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate barcode: {str(e)}")


class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x600")
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
        self.show_login_window()

    def show_login_window(self):
        for widget in self.root.winfo_children(): widget.destroy()
        LoginWindow(self.root, self.on_login_success, self.db_manager)

    def on_login_success(self, user_data):
        for widget in self.root.winfo_children(): widget.destroy()
        if user_data['role'].lower() == 'student':
            StudentDashboard(self.root, user_data, self.db_manager, self.show_login_window)
        elif user_data['role'].lower() == 'admin':
            AdminDashboard(self.root, user_data, self.db_manager, self.show_login_window)


# THIS IS THE VITAL ENGINE BLOCK THAT RUNS THE APP
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
