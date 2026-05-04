import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import hashlib
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
        self.PRIMARY_COLOR = "#DC143C"  # Crimson Red
        self.SECONDARY_COLOR = "#FFFFFF"  # White
        self.TEXT_COLOR = "#333333"
        self.LIGHT_GRAY = "#F5F5F5"
        self.ACCENT_GRAY = "#999999"
        self.BORDER_COLOR = "#E0E0E0"

        self.current_mode = "login"  # Track current mode

        # --- IMAGE LOADING ---
        try:
            # Matches your specific filename exactly
            self.original_image = Image.open("image (37).png")
        except FileNotFoundError:
            self.original_image = None
            print("Warning: image (37).png not found in the finaleproject folder.")
        self.setup_ui()

    def resize_image(self, event):
        """Dynamically scales the image when the canvas is resized."""
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

        # ===== LEFT SIDEBAR =====
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

        # --- DYNAMIC IMAGE CANVAS ---
        self.image_canvas = tk.Canvas(sidebar_content, bg=self.PRIMARY_COLOR, highlightthickness=0)
        self.image_canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(20, 0))
        self.image_canvas.bind("<Configure>", self.resize_image)

        # ===== RIGHT SECTION =====
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

        messagebox.showinfo("Success", f"Welcome {username}!")
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

        # Scanner Button Integration
        scan_btn = tk.Button(
            button_frame,
            text="📷 SCAN BOOK",
            font=("Helvetica", 11, "bold"),
            bg="#17A2B8",  # Cyan/Teal color
            fg=self.SECONDARY_COLOR,
            command=self.open_scanner,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8
        )
        scan_btn.pack(side=tk.LEFT, padx=5)

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

    # --- Scanner Methods ---
    def open_scanner(self):
        # Open the scanner window and pass the callback function
        BarcodeScannerWindow(self.root, self.handle_scanned_barcode)

        # --- Scanner Methods ---
        def open_scanner(self):
            # Open the scanner window and pass the callback function
            BarcodeScannerWindow(self.root, self.handle_scanned_barcode)

        def handle_scanned_barcode(self, scanned_isbn):
            # 1. Catch the "X" (Failed/Blurry Scan) or empty scans
            if scanned_isbn == "X" or not scanned_isbn:
                messagebox.showerror(
                    "Scan Error",
                    "The scanner couldn't read the barcode clearly. Please check the focus and lighting, then try again."
                )
                return  # Stop execution here

            # 2. Find the book with this ISBN in the treeview
            found = False
            for item in self.books_tree.get_children():
                values = self.books_tree.item(item, 'values')
                if len(values) >= 4 and values[3] == scanned_isbn:
                    # Select the item, focus it, and scroll to it
                    self.books_tree.selection_set(item)
                    self.books_tree.focus(item)
                    self.books_tree.see(item)
                    found = True

                    # Show success message
                    messagebox.showinfo("Scanner Success", f"Found book: {values[1]}")
                    break

            # 3. Handle New Books not found in the system
            if not found:
                user_wants_to_add = messagebox.askyesno(
                    "New Book Detected",
                    f"Scanned ISBN: {scanned_isbn}\n\nThis book isn't in your system yet. Would you like to add it now?"
                )
                if user_wants_to_add:
                    self.add_book(prefill_isbn=scanned_isbn)

        # --- End Scanner Methods ---

        def add_book(self, prefill_isbn=""):
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

            # Insert the scanned ISBN automatically if it was passed to the function
            if prefill_isbn:
                isbn_entry.insert(0, prefill_isbn)

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


class LibraryManagementApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#F5F5F5")

        # Initialize database
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()

        # Set application icon and style
        self.setup_styles()

        # Start with login window
        self.show_login_window()

    def setup_styles(self):
        self.root.configure(bg="#FFFFFF")
        self.color_primary = "#DC143C"  # Crimson Red
        self.color_secondary = "#FFFFFF"  # White
        self.color_text = "#333333"  # Dark text

    def show_login_window(self):
        # Clear root window
        for widget in self.root.winfo_children():
            widget.destroy()

        login_window = LoginWindow(self.root, self.on_login_success, self.db_manager)

    def on_login_success(self, user_data):
        # Convert to lowercase to catch both "Student" and "student"
        role = user_data['role'].lower()

        if role == 'student':
            self.show_student_dashboard(user_data)
        elif role == 'admin':
            self.show_admin_dashboard(user_data)

    def show_student_dashboard(self, user_data):
        # The local file import is removed, we just use the class defined above
        for widget in self.root.winfo_children():
            widget.destroy()

        dashboard = StudentDashboard(self.root, user_data, self.db_manager, self.show_login_window)

    def show_admin_dashboard(self, user_data):
        # The local file import is removed, we just use the class defined above
        for widget in self.root.winfo_children():
            widget.destroy()

        dashboard = AdminDashboard(self.root, user_data, self.db_manager, self.show_login_window)