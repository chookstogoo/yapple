import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from database import DatabaseManager
from barcode_scanner import BarcodeScannerWindow
from barcode_generator import BarcodeGenerator


class LoginWindow:
    def __init__(self, root, on_login_callback, db_manager):
        self.root = root
        self.on_login_callback = on_login_callback
        self.db_manager = db_manager

        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#333333"
        self.LIGHT_GRAY = "#F5F5F5"
        self.ACCENT_GRAY = "#999999"
        self.current_mode = "login"

        try:
            self.original_image = Image.open("image (37).png")
        except FileNotFoundError:
            self.original_image = None

        self.setup_ui()

    def resize_image(self, event):
        if not self.original_image:
            return

        new_width = event.width
        new_height = event.height

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
            self.image_canvas.create_image(new_width // 2, new_height // 2, anchor=tk.CENTER, image=self.display_image)

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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

        tk.Label(title_frame, text="📚", font=("Helvetica", 60), bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR).pack()
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
                                          bg=self.SECONDARY_COLOR, fg=self.PRIMARY_COLOR, command=self.show_login_form,
                                          relief=tk.FLAT, cursor="hand2", padx=30, pady=10, bd=0)
        self.login_toggle_btn.pack(side=tk.LEFT, padx=0)

        tk.Label(toggle_frame, text=" | ", font=("Helvetica", 16), fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.signup_toggle_btn = tk.Button(toggle_frame, text="Sign Up", font=("Helvetica", 16),
                                           bg=self.SECONDARY_COLOR, fg=self.ACCENT_GRAY, command=self.show_signup_form,
                                           relief=tk.FLAT, cursor="hand2", padx=30, pady=10, bd=0)
        self.signup_toggle_btn.pack(side=tk.LEFT, padx=0)

        self.toggle_underline = tk.Frame(self.center_container, bg=self.PRIMARY_COLOR, height=3)
        self.toggle_underline.pack(fill=tk.X, pady=(0, 20))

        self.content_frame = tk.Frame(self.center_container, bg=self.SECONDARY_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=False)

        self.show_login_form()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_login_form(self):
        self.current_mode = "login"
        self.clear_content_frame()

        self.login_toggle_btn.configure(fg=self.PRIMARY_COLOR, font=("Helvetica", 16, "bold"))
        self.signup_toggle_btn.configure(fg=self.ACCENT_GRAY, font=("Helvetica", 16))

        tk.Label(self.content_frame, text="Welcome Back!", font=("Helvetica", 20, "bold"), fg=self.PRIMARY_COLOR,
                 bg=self.SECONDARY_COLOR).pack(pady=(0, 5))
        tk.Label(self.content_frame, text="Please log in to your account", font=("Helvetica", 10), fg=self.ACCENT_GRAY,
                 bg=self.SECONDARY_COLOR).pack(pady=(0, 25))

        tk.Label(self.content_frame, text="Username", font=("Helvetica", 10, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, padx=0, pady=(0, 5))
        username_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(username_frame, text="👤", font=("Helvetica", 12), bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.login_username = tk.Entry(username_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY, border=0,
                                       fg=self.TEXT_COLOR)
        self.login_username.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.login_username.insert(0, "Enter your username")
        self.login_username.bind("<FocusIn>", lambda e: self.on_entry_focus(self.login_username, "username"))
        self.login_username.bind("<FocusOut>", lambda e: self.on_entry_blur(self.login_username, "username"))

        tk.Label(self.content_frame, text="Password", font=("Helvetica", 10, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, padx=0, pady=(0, 5))
        password_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        password_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(password_frame, text="🔒", font=("Helvetica", 12), bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.login_password = tk.Entry(password_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY, border=0,
                                       fg=self.TEXT_COLOR, show="*")
        self.login_password.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.login_password.insert(0, "Enter your password")
        self.login_password.bind("<FocusIn>", lambda e: self.on_entry_focus(self.login_password, "password"))
        self.login_password.bind("<FocusOut>", lambda e: self.on_entry_blur(self.login_password, "password"))

        tk.Label(self.content_frame, text="Role", font=("Helvetica", 10, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, padx=0, pady=(0, 5))
        role_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        role_frame.pack(fill=tk.X, pady=(0, 25))
        tk.Label(role_frame, text="🛡️", font=("Helvetica", 12), bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.login_role = ttk.Combobox(role_frame, values=["Student", "Admin"], state="readonly",
                                       font=("Helvetica", 11), width=25)
        self.login_role.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 10))
        self.login_role.set("Student")

        login_submit_btn = tk.Button(self.content_frame, text="Log In", font=("Helvetica", 12, "bold"),
                                     bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR, command=self.perform_login,
                                     relief=tk.FLAT, cursor="hand2", padx=20, pady=12)
        login_submit_btn.pack(fill=tk.X, pady=(0, 15))

        sep_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        sep_frame.pack(fill=tk.X, pady=10)
        tk.Label(sep_frame, text="or", font=("Helvetica", 10), fg=self.ACCENT_GRAY, bg=self.SECONDARY_COLOR).pack()

        signup_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        signup_frame.pack(pady=(0, 20))
        tk.Label(signup_frame, text="Don't have an account? ", font=("Helvetica", 10), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(side=tk.LEFT)
        signup_link = tk.Label(signup_frame, text="Sign Up", font=("Helvetica", 10, "bold"), fg=self.PRIMARY_COLOR,
                               bg=self.SECONDARY_COLOR, cursor="hand2")
        signup_link.pack(side=tk.LEFT)
        signup_link.bind("<Button-1>", lambda e: self.show_signup_form())

    def show_signup_form(self):
        self.current_mode = "signup"
        self.clear_content_frame()

        self.login_toggle_btn.configure(fg=self.ACCENT_GRAY, font=("Helvetica", 16))
        self.signup_toggle_btn.configure(fg=self.PRIMARY_COLOR, font=("Helvetica", 16, "bold"))

        tk.Label(self.content_frame, text="Create Account", font=("Helvetica", 20, "bold"), fg=self.PRIMARY_COLOR,
                 bg=self.SECONDARY_COLOR).pack(pady=(0, 5))
        tk.Label(self.content_frame, text="Join our library community", font=("Helvetica", 10), fg=self.ACCENT_GRAY,
                 bg=self.SECONDARY_COLOR).pack(pady=(0, 25))

        tk.Label(self.content_frame, text="Username", font=("Helvetica", 10, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, padx=0, pady=(0, 5))
        username_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(username_frame, text="👤", font=("Helvetica", 12), bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.signup_username = tk.Entry(username_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY, border=0,
                                        fg=self.TEXT_COLOR)
        self.signup_username.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.signup_username.insert(0, "Enter your username")
        self.signup_username.bind("<FocusIn>", lambda e: self.on_entry_focus(self.signup_username, "username"))
        self.signup_username.bind("<FocusOut>", lambda e: self.on_entry_blur(self.signup_username, "username"))

        tk.Label(self.content_frame, text="Password", font=("Helvetica", 10, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, padx=0, pady=(0, 5))
        password_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        password_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(password_frame, text="🔒", font=("Helvetica", 12), bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.signup_password = tk.Entry(password_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY, border=0,
                                        fg=self.TEXT_COLOR, show="*")
        self.signup_password.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.signup_password.insert(0, "Enter your password")
        self.signup_password.bind("<FocusIn>", lambda e: self.on_entry_focus(self.signup_password, "password"))
        self.signup_password.bind("<FocusOut>", lambda e: self.on_entry_blur(self.signup_password, "password"))

        tk.Label(self.content_frame, text="Confirm Password", font=("Helvetica", 10, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, padx=0, pady=(0, 5))
        confirm_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        confirm_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(confirm_frame, text="🔒", font=("Helvetica", 12), bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.signup_confirm = tk.Entry(confirm_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY, border=0,
                                       fg=self.TEXT_COLOR, show="*")
        self.signup_confirm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.signup_confirm.insert(0, "Confirm your password")
        self.signup_confirm.bind("<FocusIn>", lambda e: self.on_entry_focus(self.signup_confirm, "confirm"))
        self.signup_confirm.bind("<FocusOut>", lambda e: self.on_entry_blur(self.signup_confirm, "confirm"))

        tk.Label(self.content_frame, text="Role", font=("Helvetica", 10, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, padx=0, pady=(0, 5))
        role_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        role_frame.pack(fill=tk.X, pady=(0, 25))
        tk.Label(role_frame, text="🛡️", font=("Helvetica", 12), bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(
            side=tk.LEFT, padx=10)

        self.signup_role = ttk.Combobox(role_frame, values=["Student", "Admin"], state="readonly",
                                        font=("Helvetica", 11), width=25)
        self.signup_role.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 10))
        self.signup_role.set("Student")

        signup_submit_btn = tk.Button(self.content_frame, text="Sign Up", font=("Helvetica", 12, "bold"),
                                      bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR, command=self.perform_signup,
                                      relief=tk.FLAT, cursor="hand2", padx=20, pady=12)
        signup_submit_btn.pack(fill=tk.X, pady=(0, 15))

        sep_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        sep_frame.pack(fill=tk.X, pady=10)
        tk.Label(sep_frame, text="or", font=("Helvetica", 10), fg=self.ACCENT_GRAY, bg=self.SECONDARY_COLOR).pack()

        login_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        login_frame.pack(pady=(0, 20))
        tk.Label(login_frame, text="Already have an account? ", font=("Helvetica", 10), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(side=tk.LEFT)
        login_link = tk.Label(login_frame, text="Log In", font=("Helvetica", 10, "bold"), fg=self.PRIMARY_COLOR,
                              bg=self.SECONDARY_COLOR, cursor="hand2")
        login_link.pack(side=tk.LEFT)
        login_link.bind("<Button-1>", lambda e: self.show_login_form())

    def on_entry_focus(self, entry, field_type):
        if field_type == "username" and entry.get() == "Enter your username":
            entry.delete(0, tk.END)
        elif field_type == "password" and entry.get() == "Enter your password":
            entry.delete(0, tk.END)
        elif field_type == "confirm" and entry.get() == "Confirm your password":
            entry.delete(0, tk.END)

    def on_entry_blur(self, entry, field_type):
        if field_type == "username" and entry.get() == "":
            entry.insert(0, "Enter your username")
        elif field_type == "password" and entry.get() == "":
            entry.insert(0, "Enter your password")
        elif field_type == "confirm" and entry.get() == "":
            entry.insert(0, "Confirm your password")

    def perform_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        role = self.login_role.get()

        if username == "Enter your username" or not username:
            messagebox.showerror("Error", "Please enter your username")
            return
        if password == "Enter your password" or not password:
            messagebox.showerror("Error", "Please enter your password")
            return
        if not role:
            messagebox.showerror("Error", "Please select a role")
            return

        user = self.db_manager.authenticate_user(username, password)
        if not user:
            messagebox.showerror("Error", "Invalid username or password")
            return
        if user['role'] != role:
            messagebox.showerror("Error", f"This account is registered as {user['role']}")
            return

        self.on_login_callback(user)

    def perform_signup(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()
        confirm = self.signup_confirm.get().strip()
        role = self.signup_role.get()

        if username == "Enter your username" or not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        if password == "Enter your password" or not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        if confirm == "Confirm your password" or not confirm:
            messagebox.showerror("Error", "Please confirm your password")
            return
        if not role:
            messagebox.showerror("Error", "Please select a role")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return

        existing_user = self.db_manager.get_user_by_username(username)
        if existing_user:
            messagebox.showerror("Error", "Username already exists")
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
        self.barcode_generator = BarcodeGenerator()

        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#333333"
        self.ACCENT_COLOR = "#F5F5F5"
        self.BG_COLOR = "#F5F5F5"

        self.setup_ui()

    def on_admin_tree_double_click(self, event):
        widget = event.widget
        selection = widget.selection()
        if not selection:
            return

        item = selection[0]
        values = widget.item(item, 'values')

        title = None
        if widget == getattr(self, 'status_tree', None):
            title = values[0]
        elif widget == getattr(self, 'transactions_tree', None):
            title = values[2]
        elif widget == getattr(self, 'requests_tree', None):
            title = values[2]

        if title:
            books = self.db_manager.get_all_books()
            for b in books:
                if b['title'] == title:
                    self.show_barcode(b['book_id'], b['title'], b['author'], b['isbn'])
                    break

    def setup_ui(self):
        self.root.configure(bg=self.SECONDARY_COLOR)

        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text=f"👨‍💼 Welcome, {self.user_data['username']}! (Admin)",
                         font=("Helvetica", 16, "bold"), fg=self.SECONDARY_COLOR, bg=self.PRIMARY_COLOR)
        title.pack(side=tk.LEFT, padx=20, pady=20)

        logout_btn = tk.Button(header, text="LOGOUT", font=("Helvetica", 10, "bold"), bg=self.SECONDARY_COLOR,
                               fg=self.PRIMARY_COLOR, command=self.logout, relief=tk.FLAT, cursor="hand2", padx=15,
                               pady=5)
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

        self.requests_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.requests_tab, text="🔔 Pending Requests")
        self.setup_requests_tab()

    def setup_book_management_tab(self):
        button_frame = tk.Frame(self.book_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(button_frame, text="➕ ADD NEW BOOK", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=self.add_book, relief=tk.FLAT, cursor="hand2", padx=15, pady=8).pack(
            side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="🗑️ DELETE BOOK", font=("Helvetica", 11, "bold"), bg="#DC3545",
                  fg=self.SECONDARY_COLOR, command=self.delete_book, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="✏️ UPDATE BOOK", font=("Helvetica", 11, "bold"), bg="#FFC107",
                  fg=self.TEXT_COLOR, command=self.update_book, relief=tk.FLAT, cursor="hand2", padx=15, pady=8).pack(
            side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="🔄 REFRESH", font=("Helvetica", 11, "bold"), bg="#28A745",
                  fg=self.SECONDARY_COLOR, command=self.load_books, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="📷 SCAN BOOK", font=("Helvetica", 11, "bold"), bg="#17A2B8",
                  fg=self.SECONDARY_COLOR, command=self.open_scanner, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

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
        self.books_tree.bind('<Double-1>', self.on_book_selected)

        self.load_books()

    def open_scanner(self):
        BarcodeScannerWindow(self.root, self.handle_scanned_barcode)

    def handle_scanned_barcode(self, scanned_isbn):
        if scanned_isbn == "X" or not scanned_isbn:
            self.root.after(100, lambda: messagebox.showerror("Scan Error",
                                                              "The scanner couldn't read the barcode clearly."))
            return

        found = False
        for item in self.books_tree.get_children():
            values = self.books_tree.item(item, 'values')
            if len(values) >= 4 and values[3] == scanned_isbn:
                self.books_tree.selection_set(item)
                self.books_tree.focus(item)
                self.books_tree.see(item)
                found = True
                self.root.after(100, lambda: messagebox.showinfo("Scanner Success", f"Found book: {values[1]}"))
                break

        if not found:
            def ask_to_add():
                if messagebox.askyesno("New Book Detected", f"Scanned ISBN: {scanned_isbn}\n\nAdd this book now?"):
                    self.add_book(prefill_isbn=scanned_isbn)

            self.root.after(100, ask_to_add)

    def setup_book_status_tab(self):
        status_frame = tk.Frame(self.status_tab, bg=self.SECONDARY_COLOR)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(status_frame, text="📊 LIBRARY STATISTICS", font=("Helvetica", 14, "bold"), fg=self.PRIMARY_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, pady=(0, 20))

        stats_container = tk.Frame(status_frame, bg=self.SECONDARY_COLOR)
        stats_container.pack(fill=tk.X, pady=10)

        self.total_books_label = tk.Label(stats_container, text="Total Books: 0", font=("Helvetica", 12, "bold"),
                                          fg=self.SECONDARY_COLOR, bg=self.PRIMARY_COLOR, padx=20, pady=20,
                                          relief=tk.RAISED, bd=2)
        self.total_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.available_books_label = tk.Label(stats_container, text="Available Books: 0",
                                              font=("Helvetica", 12, "bold"), fg=self.SECONDARY_COLOR, bg="#28A745",
                                              padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.available_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.borrowed_books_label = tk.Label(stats_container, text="Borrowed Books: 0", font=("Helvetica", 12, "bold"),
                                             fg=self.SECONDARY_COLOR, bg="#007BFF", padx=20, pady=20, relief=tk.RAISED,
                                             bd=2)
        self.borrowed_books_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        tk.Label(status_frame, text="\n📖 Individual Book Status:", font=("Helvetica", 12, "bold"), fg=self.TEXT_COLOR,
                 bg=self.SECONDARY_COLOR).pack(anchor=tk.W, pady=(20, 10))

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
        self.status_tree.bind('<Double-1>', self.on_admin_tree_double_click)

        tk.Button(status_frame, text="🔄 REFRESH STATS", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=self.load_book_status, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(pady=(20, 0))

        self.load_book_status()

    def setup_transactions_tab(self):
        button_frame = tk.Frame(self.transaction_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(button_frame, text="🔄 REFRESH TRANSACTIONS", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=self.load_transactions, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.transaction_tab, bg=self.SECONDARY_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "User", "Book Title", "Type", "Quantity", "Date", "Due Date", "Status")
        self.transactions_tree = ttk.Treeview(tree_frame, columns=columns, height=15, show="headings")

        for col in columns:
            self.transactions_tree.heading(col, text=col)
            if col == "ID":
                self.transactions_tree.column(col, width=30)
            elif col in ("Type", "Quantity", "Date", "Due Date", "Status"):
                self.transactions_tree.column(col, width=85)
            else:
                self.transactions_tree.column(col, width=100)

        self.transactions_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transactions_tree.configure(yscroll=scrollbar.set)
        self.transactions_tree.bind('<Double-1>', self.on_admin_tree_double_click)

        self.load_transactions()

    def setup_requests_tab(self):
        button_frame = tk.Frame(self.requests_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(button_frame, text="✅ APPROVE", font=("Helvetica", 11, "bold"), bg="#28A745",
                  fg=self.SECONDARY_COLOR, command=self.approve_request, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="❌ REJECT SELECTED", font=("Helvetica", 11, "bold"), bg="#DC3545",
                  fg=self.SECONDARY_COLOR, command=self.reject_request, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="🔄 REFRESH", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=self.load_requests, relief=tk.FLAT, cursor="hand2", padx=15,
                  pady=8).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.requests_tab, bg=self.SECONDARY_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # FIXED: Added Barcode explicitly to columns
        columns = ("Req ID", "User", "Book Title", "Qty", "Status", "Barcode")
        self.requests_tree = ttk.Treeview(tree_frame, columns=columns, height=15, show="headings")

        for col in columns:
            self.requests_tree.heading(col, text=col)
            if col == "Req ID" or col == "Qty":
                self.requests_tree.column(col, width=50)
            elif col == "Barcode":
                self.requests_tree.column(col, width=120)
            else:
                self.requests_tree.column(col, width=100)

        self.requests_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.requests_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.requests_tree.configure(yscroll=scrollbar.set)
        self.requests_tree.bind('<Double-1>', self.on_admin_tree_double_click)

        self.load_requests()

    def load_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        books = self.db_manager.get_all_books()
        for book in books:
            self.books_tree.insert('', tk.END, values=(
                book['book_id'], book['title'], book['author'],
                book['isbn'], book['quantity'], book['available_quantity']
            ))

    def on_book_selected(self, event):
        selection = self.books_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')

        if len(values) >= 4:
            book_id, title, author, isbn = values[0], values[1], values[2], values[3]
            self.show_barcode(int(book_id), title, author, isbn)

    def show_barcode(self, book_id, title, author, isbn):
        barcode_window = tk.Toplevel(self.root)
        barcode_window.title("Book Info")
        barcode_window.geometry("380x420")
        barcode_window.configure(bg=self.BG_COLOR)
        barcode_window.resizable(False, False)

        header = tk.Frame(barcode_window, bg=self.PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Book Details & Barcode", font=("Segoe UI", 12, "bold"), fg="#FFFFFF",
                 bg=self.PRIMARY_COLOR).pack(pady=10)

        content = tk.Frame(barcode_window, bg=self.BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        info_frame = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        info_frame.pack(fill=tk.X, pady=(0, 12))

        info_items = [("Title:", title[:35]), ("Author:", author[:30]), ("ISBN:", isbn), ("Book ID:", str(book_id))]

        for label_text, value_text in info_items:
            item_frame = tk.Frame(info_frame, bg=self.SECONDARY_COLOR)
            item_frame.pack(fill=tk.X, padx=10, pady=4)
            tk.Label(item_frame, text=label_text, font=("Segoe UI", 10, "bold"), fg=self.PRIMARY_COLOR,
                     bg=self.SECONDARY_COLOR, width=8, anchor="w").pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(item_frame, text=value_text, font=("Segoe UI", 10), fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR,
                     wraplength=230, justify=tk.LEFT).pack(side=tk.LEFT)

        barcode_section = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        barcode_section.pack(fill=tk.BOTH, expand=True, pady=8)
        barcode_label = tk.Label(barcode_section, bg=self.SECONDARY_COLOR)
        barcode_label.pack(pady=15)

        try:
            barcode_image = self.barcode_generator.generate_barcode(str(isbn))
            barcode_photo = ImageTk.PhotoImage(barcode_image)
            barcode_label.config(image=barcode_photo)
            barcode_label.image = barcode_photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate barcode: {str(e)}")

    def load_requests(self):
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)

        try:
            requests = self.db_manager.get_pending_requests()
            for req in requests:
                barcode = req.get('barcode', req.get('isbn', 'N/A'))
                self.requests_tree.insert('', tk.END, values=(
                    req['transaction_id'], req['username'], req['title'], req['qty_requested'], "Pending", barcode
                ))
        except Exception as e:
            pass

    def approve_request(self):
        selection = self.requests_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a request to approve.")
            return

        req_id = int(self.requests_tree.item(selection[0], 'values')[0])
        pending = self.db_manager.get_pending_requests()
        req = next((r for r in pending if r['transaction_id'] == req_id), None)

        if req:
            try:
                self.db_manager.admin_approve_request(req['transaction_id'], req['user_id'], req['book_id'],
                                                      req['qty_requested'])
                messagebox.showinfo("Success", "Request Approved.")
                self.load_requests()
                self.load_book_status()
                self.load_books()
                self.load_transactions()
            except Exception as e:
                messagebox.showerror("Error", f"Could not approve: {e}")
        else:
            messagebox.showerror("Error", "Request not found.")

    def reject_request(self):
        selection = self.requests_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a request to reject.")
            return

        # Explicitly converting this to an integer fixes the silent crash
        req_id = int(self.requests_tree.item(selection[0], 'values')[0])
        try:
            self.db_manager.update_request_status(req_id, "Rejected")
            messagebox.showinfo("Success", "Request Rejected.")
            self.load_requests()
        except Exception as e:
            messagebox.showerror("Error", f"Could not reject: {e}")

    def add_book(self, prefill_isbn=""):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Book")
        add_window.geometry("400x350")
        add_window.configure(bg=self.SECONDARY_COLOR)

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

        tk.Button(add_window, text="SAVE BOOK", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=save_book, relief=tk.FLAT, cursor="hand2", padx=20, pady=10).pack(
            pady=20)

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

        tk.Button(update_window, text="UPDATE BOOK", font=("Helvetica", 11, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=save_update, relief=tk.FLAT, cursor="hand2", padx=20, pady=10).pack(
            pady=20)

    def load_book_status(self):
        books = self.db_manager.get_all_books()
        total_qty = sum(book['quantity'] for book in books)
        available_qty = sum(book['available_quantity'] for book in books)
        borrowed_qty = total_qty - available_qty

        self.total_books_label.config(text=f"Total Books: {total_qty}")
        self.available_books_label.config(text=f"Available Books: {available_qty}")
        self.borrowed_books_label.config(text=f"Borrowed Books: {borrowed_qty}")

        for item in self.status_tree.get_children():
            self.status_tree.delete(item)

        for book in books:
            borrowed = book['quantity'] - book['available_quantity']
            self.status_tree.insert('', tk.END,
                                    values=(book['title'], book['author'], book['quantity'], book['available_quantity'],
                                            borrowed))

    def load_transactions(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        transactions = self.db_manager.get_all_transactions()
        for trans in transactions:
            due_date = trans['due_date'] if trans['due_date'] else "N/A"
            quantity = trans.get('quantity', 1) if trans.get('quantity') else 1
            status = trans.get('status', 'Unknown')

            self.transactions_tree.insert('', tk.END, values=(
                trans['transaction_id'], trans['username'], trans['title'],
                trans['transaction_type'].upper(), quantity, trans['transaction_date'][:10],
                due_date[:10] if due_date != "N/A" else "N/A", status
            ))

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

        self.cart_items = []

        self.BG_COLOR = "#F5F5F5"
        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#333333"

        self.root.configure(bg=self.BG_COLOR)
        self.root.geometry("900x600")
        self.root.minsize(900, 600)

        self.setup_ui()
        self.load_books()
        self.load_transactions()

        self.auto_update_transactions()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text=f"Welcome, {self.user_data['username']}!", bg=self.PRIMARY_COLOR, fg="#FFFFFF",
                 font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=20, pady=15)

        tk.Button(header, text="Logout", bg=self.SECONDARY_COLOR, fg=self.TEXT_COLOR, relief=tk.FLAT,
                  command=self.logout_callback).pack(side=tk.RIGHT, padx=20, pady=15)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=self.BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.SECONDARY_COLOR, foreground=self.TEXT_COLOR, padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", self.PRIMARY_COLOR)], foreground=[("selected", "#FFFFFF")])

        style.configure("Treeview", background=self.SECONDARY_COLOR, foreground=self.TEXT_COLOR,
                        fieldbackground=self.SECONDARY_COLOR, borderwidth=0)
        style.configure("Treeview.Heading", background=self.PRIMARY_COLOR, foreground="#FFFFFF", relief=tk.FLAT)
        style.map("Treeview", background=[("selected", "#E0E0E0")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))

        # --- TAB 1: Library Books ---
        self.books_frame = tk.Frame(self.notebook, bg=self.BG_COLOR)
        self.notebook.add(self.books_frame, text="Library Books")

        books_top = tk.Frame(self.books_frame, bg=self.BG_COLOR)
        books_top.pack(fill=tk.X, pady=10)

        tk.Button(books_top, text="↻ Refresh List", bg=self.PRIMARY_COLOR, fg="#FFFFFF", relief=tk.FLAT,
                  command=self.load_books).pack(side=tk.LEFT, padx=10)
        tk.Label(books_top, text="(Double-click a book to view its Barcode)", bg=self.BG_COLOR, fg="#555555").pack(
            side=tk.LEFT, padx=10)

        columns = ('ID', 'Title', 'Author', 'ISBN', 'Available')
        self.books_tree = ttk.Treeview(self.books_frame, columns=columns, show='headings')

        for col in columns:
            self.books_tree.heading(col, text=col)

        self.books_tree.column('ID', width=50, anchor=tk.CENTER)
        self.books_tree.column('Title', width=300)
        self.books_tree.column('Author', width=200)
        self.books_tree.column('ISBN', width=150)
        self.books_tree.column('Available', width=100, anchor=tk.CENTER)

        self.books_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.books_tree.bind('<Double-1>', self.on_book_selected)

        # --- TAB 2: My Transactions ---
        self.trans_frame = tk.Frame(self.notebook, bg=self.BG_COLOR)
        self.notebook.add(self.trans_frame, text="My Transactions")

        t_columns = ('Trans ID', 'Title', 'Quantity', 'Borrowed Date', 'Due Date', 'Status')
        self.trans_tree = ttk.Treeview(self.trans_frame, columns=t_columns, show='headings')

        self.trans_tree.heading('Trans ID', text='ID')
        self.trans_tree.heading('Title', text='Book Title')
        self.trans_tree.heading('Quantity', text='Quantity')
        self.trans_tree.heading('Borrowed Date', text='Request Date')
        self.trans_tree.heading('Due Date', text='Due Date')
        self.trans_tree.heading('Status', text='Status')

        self.trans_tree.column('Trans ID', width=50, anchor=tk.CENTER)
        self.trans_tree.column('Title', width=280)
        self.trans_tree.column('Quantity', width=70, anchor=tk.CENTER)
        self.trans_tree.column('Borrowed Date', width=120)
        self.trans_tree.column('Due Date', width=120)
        self.trans_tree.column('Status', width=100, anchor=tk.CENTER)

        self.trans_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(20, 5))

        # FIXED: Added the Return UI explicitly into the student dashboard
        ret_frame = tk.Frame(self.trans_frame, bg=self.BG_COLOR)
        ret_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(ret_frame, text="Note: Only 'Active' (approved) books can be returned.", bg=self.BG_COLOR,
                 fg="#555555", font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=10)
        tk.Button(ret_frame, text="Return Selected Book", bg="#28A745", fg="#FFFFFF", relief=tk.FLAT,
                  font=("Segoe UI", 11, "bold"), command=self.process_return).pack(side=tk.RIGHT, padx=10)

        # --- BOTTOM SECTION: Request Book Form ---
        self.request_frame = tk.Frame(self.root, bg=self.SECONDARY_COLOR, height=130)
        self.request_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(0, 20))
        self.request_frame.pack_propagate(False)

        top_req = tk.Frame(self.request_frame, bg=self.SECONDARY_COLOR)
        top_req.pack(fill=tk.X, pady=10, padx=10)

        tk.Label(top_req, text="Request Book:", bg=self.SECONDARY_COLOR, fg=self.TEXT_COLOR,
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.book_combo = ttk.Combobox(top_req, width=40, state="readonly")
        self.book_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(top_req, text="Qty:", bg=self.SECONDARY_COLOR, fg=self.TEXT_COLOR, font=("Segoe UI", 10, "bold")).pack(
            side=tk.LEFT, padx=5)
        self.qty_entry = tk.Entry(top_req, width=5)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(top_req, text="Add to Cart", bg=self.PRIMARY_COLOR, fg="#FFFFFF", relief=tk.FLAT,
                  command=self.add_to_cart).pack(side=tk.LEFT, padx=10)

        bottom_req = tk.Frame(self.request_frame, bg=self.SECONDARY_COLOR)
        bottom_req.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        self.cart_text = tk.Text(bottom_req, height=3, width=60, bg=self.BG_COLOR, fg=self.TEXT_COLOR,
                                 state=tk.DISABLED)
        self.cart_text.pack(side=tk.LEFT, fill=tk.Y)

        # FIXED: Hard-blocked the mouse pasting triggers (middle and right clicks) along with typing
        self.cart_text.bind("<Key>", lambda e: "break")
        self.cart_text.bind("<Button-2>", lambda e: "break")
        self.cart_text.bind("<Button-3>", lambda e: "break")

        tk.Button(bottom_req, text="Submit Request to Admin", bg="#28A745", fg="#FFFFFF", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, command=self.submit_request).pack(side=tk.LEFT, padx=20)

    def load_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        books = self.db_manager.get_all_books()
        combo_values = []

        for b in books:
            self.books_tree.insert('', tk.END, values=(
                b['book_id'], b['title'], b['author'], b['isbn'], b['available_quantity']
            ))
            combo_values.append(f"[{b['book_id']}] {b['title']} (Avail: {b['available_quantity']})")

        self.book_combo['values'] = combo_values

    def _sync_cart_visibility(self):
        try:
            if self.cart_items:
                self.cart_text.pack(fill=tk.BOTH, expand=True)
            else:
                self.cart_text.pack_forget()
        except Exception:
            pass

    def add_to_cart(self):
        book_selection = self.book_combo.get()
        qty = self.qty_entry.get()

        if not book_selection:
            messagebox.showwarning("Warning", "Please select a book from the dropdown.")
            self._sync_cart_visibility()
            return

        if not qty.isdigit() or int(qty) <= 0:
            messagebox.showwarning("Warning", "Quantity must be a valid number greater than 0.")
            self._sync_cart_visibility()
            return

        avail_qty = int(book_selection.split("(Avail: ")[1].replace(")", "").strip())
        req_qty = int(qty)

        if req_qty > avail_qty:
            messagebox.showerror("Error",
                                 f"Not enough books available to borrow! You requested {req_qty}, but only {avail_qty} are available.")
            self.qty_entry.delete(0, tk.END)
            self.qty_entry.insert(0, "1")
            self._sync_cart_visibility()
            return

        book_title = book_selection.split("]")[1].split("(Avail")[0].strip()

        self.cart_text.config(state=tk.NORMAL)
        self.cart_text.insert(tk.END, f"{book_title} (Qty: {qty})\n")
        self.cart_text.config(state=tk.DISABLED)
        self.cart_items.append((book_selection, req_qty))

        self.book_combo.set('')
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        self._sync_cart_visibility()

    def submit_request(self):
        if not self.cart_items:
            messagebox.showwarning("Empty Cart", "Please add a book to the cart before submitting.")
            return

        try:
            for book_str, qty in self.cart_items:
                book_id_str = book_str.split("]")[0].replace("[", "")
                book_id = int(book_id_str)
                self.db_manager.add_book_request(self.user_data['user_id'], book_id, qty)

            messagebox.showinfo("Success", "Request sent to Admin successfully!")

            self.cart_text.config(state=tk.NORMAL)
            self.cart_text.delete(1.0, tk.END)
            self.cart_text.config(state=tk.DISABLED)
            self.cart_items.clear()
            self._sync_cart_visibility()

            self.load_transactions()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit: {str(e)}")

    def load_transactions(self):
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)

        borrowed = self.db_manager.get_user_borrowed_books(self.user_data['user_id'])
        for t in borrowed:
            borrow_date = str(t['transaction_date'])[:16] if t['transaction_date'] else "N/A"
            due_date = str(t['due_date'])[:16] if t['due_date'] else "N/A"
            status = t.get('status', 'Unknown')
            quantity = t.get('quantity', 1)

            self.trans_tree.insert('', tk.END,
                                   values=(t['transaction_id'], t['title'], quantity, borrow_date, due_date, status))

    def process_return(self):
        selected = self.trans_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book from the list to return.")
            return

        values = self.trans_tree.item(selected[0], 'values')
        trans_id = values[0]
        status = values[5]

        if status != 'Active':
            messagebox.showwarning("Warning",
                                   "Only 'Active' (approved) books can be returned.\nPending requests cannot be returned.")
            return

        borrowed = self.db_manager.get_user_borrowed_books(self.user_data['user_id'])
        t = next((x for x in borrowed if str(x['transaction_id']) == str(trans_id)), None)

        if t:
            self.db_manager.return_book(t['transaction_id'], t['book_id'], str(t.get('quantity', 1)))
            messagebox.showinfo("Success", "Book returned successfully!")
            self.load_transactions()
            self.load_books()

    def auto_update_transactions(self):
        self.load_transactions()
        self.root.after(5000, self.auto_update_transactions)

    def on_book_selected(self, event):
        selection = self.books_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')

        if len(values) >= 4:
            book_id, title, author, isbn = values[0], values[1], values[2], values[3]
            self.show_barcode(int(book_id), title, author, isbn)

    def show_barcode(self, book_id, title, author, isbn):
        barcode_window = tk.Toplevel(self.root)
        barcode_window.title("Book Info")
        barcode_window.geometry("380x420")
        barcode_window.configure(bg=self.BG_COLOR)
        barcode_window.resizable(False, False)

        header = tk.Frame(barcode_window, bg=self.PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Book Details & Barcode", font=("Segoe UI", 12, "bold"), fg="#FFFFFF",
                 bg=self.PRIMARY_COLOR).pack(pady=10)

        content = tk.Frame(barcode_window, bg=self.BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        info_frame = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        info_frame.pack(fill=tk.X, pady=(0, 12))

        info_items = [("Title:", title[:35]), ("Author:", author[:30]), ("ISBN:", isbn), ("Book ID:", str(book_id))]

        for label_text, value_text in info_items:
            item_frame = tk.Frame(info_frame, bg=self.SECONDARY_COLOR)
            item_frame.pack(fill=tk.X, padx=10, pady=4)
            tk.Label(item_frame, text=label_text, font=("Segoe UI", 10, "bold"), fg=self.PRIMARY_COLOR,
                     bg=self.SECONDARY_COLOR, width=8, anchor="w").pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(item_frame, text=value_text, font=("Segoe UI", 10), fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR,
                     wraplength=230, justify=tk.LEFT).pack(side=tk.LEFT)

        barcode_section = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        barcode_section.pack(fill=tk.BOTH, expand=True, pady=8)
        barcode_label = tk.Label(barcode_section, bg=self.SECONDARY_COLOR)
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
        self.root.configure(bg="#F5F5F5")

        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()

        self.setup_styles()
        self.show_login_window()

    def setup_styles(self):
        self.root.configure(bg="#FFFFFF")

    def show_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        login_window = LoginWindow(self.root, self.on_login_success, self.db_manager)

    def on_login_success(self, user_data):
        role = user_data['role'].lower()
        if role == 'student':
            self.show_student_dashboard(user_data)
        elif role == 'admin':
            self.show_admin_dashboard(user_data)

    def show_student_dashboard(self, user_data):
        for widget in self.root.winfo_children():
            widget.destroy()
        dashboard = StudentDashboard(self.root, user_data, self.db_manager, self.show_login_window)

    def show_admin_dashboard(self, user_data):
        for widget in self.root.winfo_children():
            widget.destroy()
        dashboard = AdminDashboard(self.root, user_data, self.db_manager, self.show_login_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()