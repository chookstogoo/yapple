import tkinter as tk
from tkinter import ttk, messagebox
import hashlib


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
        self.setup_ui()

    def setup_ui(self):
        # Clear root
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.SECONDARY_COLOR)

        # Main container with two sections
        main_container = tk.Frame(self.root, bg=self.SECONDARY_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)

        # ===== LEFT SIDEBAR =====
        left_sidebar = tk.Frame(main_container, bg=self.PRIMARY_COLOR, width=400)
        left_sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_sidebar.pack_propagate(False)

        # Sidebar content
        sidebar_content = tk.Frame(left_sidebar, bg=self.PRIMARY_COLOR)
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=40)

        # Library icon and title
        title_frame = tk.Frame(sidebar_content, bg=self.PRIMARY_COLOR)
        title_frame.pack(pady=(0, 40))

        tk.Label(
            title_frame,
            text="📚",
            font=("Helvetica", 60),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR
        ).pack()

        tk.Label(
            title_frame,
            text="LIBRARY",
            font=("Helvetica", 32, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR
        ).pack()

        tk.Label(
            title_frame,
            text="MANAGEMENT SYSTEM",
            font=("Helvetica", 12),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR
        ).pack()

        # Separator
        tk.Label(
            sidebar_content,
            text="━" * 30,
            font=("Helvetica", 10),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR
        ).pack(pady=20)

        # Features
        features = [
            "Manage Books",
            "Manage Users",
            "Manage Knowledge"
        ]

        for feature_text in features:
            feature_frame = tk.Frame(sidebar_content, bg=self.PRIMARY_COLOR)
            feature_frame.pack(pady=15, anchor=tk.W)

            tk.Label(
                feature_frame,
                text=f"● {feature_text}",
                font=("Helvetica", 13),
                bg=self.PRIMARY_COLOR,
                fg=self.SECONDARY_COLOR
            ).pack()

        # ===== RIGHT SECTION =====
        right_section = tk.Frame(main_container, bg=self.SECONDARY_COLOR)
        right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Outer centering frame
        outer_frame = tk.Frame(right_section, bg=self.SECONDARY_COLOR)
        outer_frame.pack(fill=tk.BOTH, expand=True)

        # Inner centered container (will hold the form)
        self.center_container = tk.Frame(outer_frame, bg=self.SECONDARY_COLOR)
        self.center_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380)

        # Toggle buttons (Log In / Sign Up)
        toggle_frame = tk.Frame(self.center_container, bg=self.SECONDARY_COLOR)
        toggle_frame.pack(fill=tk.X, pady=(0, 30))

        self.login_toggle_btn = tk.Button(
            toggle_frame,
            text="Log In",
            font=("Helvetica", 16, "bold"),
            bg=self.SECONDARY_COLOR,
            fg=self.PRIMARY_COLOR,
            command=self.show_login_form,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=10,
            bd=0
        )
        self.login_toggle_btn.pack(side=tk.LEFT, padx=0)

        tk.Label(toggle_frame, text=" | ", font=("Helvetica", 16),
                 fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.signup_toggle_btn = tk.Button(
            toggle_frame,
            text="Sign Up",
            font=("Helvetica", 16),
            bg=self.SECONDARY_COLOR,
            fg=self.ACCENT_GRAY,
            command=self.show_signup_form,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=10,
            bd=0
        )
        self.signup_toggle_btn.pack(side=tk.LEFT, padx=0)

        # Underline for toggle
        self.toggle_underline = tk.Frame(self.center_container, bg=self.PRIMARY_COLOR, height=3)
        self.toggle_underline.pack(fill=tk.X, pady=(0, 20))

        # Content frame for switching between login/signup
        self.content_frame = tk.Frame(self.center_container, bg=self.SECONDARY_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=False)

        # Show login form by default
        self.show_login_form()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_login_form(self):
        self.current_mode = "login"
        self.clear_content_frame()

        # Update toggle buttons
        self.login_toggle_btn.configure(fg=self.PRIMARY_COLOR, font=("Helvetica", 16, "bold"))
        self.signup_toggle_btn.configure(fg=self.ACCENT_GRAY, font=("Helvetica", 16))

        # Welcome message
        tk.Label(
            self.content_frame,
            text="Welcome Back!",
            font=("Helvetica", 20, "bold"),
            fg=self.PRIMARY_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(pady=(0, 5))

        tk.Label(
            self.content_frame,
            text="Please log in to your account",
            font=("Helvetica", 10),
            fg=self.ACCENT_GRAY,
            bg=self.SECONDARY_COLOR
        ).pack(pady=(0, 25))

        # Username field
        tk.Label(
            self.content_frame,
            text="Username",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(anchor=tk.W, padx=0, pady=(0, 5))

        username_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(username_frame, text="👤", font=("Helvetica", 12),
                 bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.login_username = tk.Entry(
            username_frame,
            font=("Helvetica", 11),
            bg=self.LIGHT_GRAY,
            border=0,
            fg=self.TEXT_COLOR
        )
        self.login_username.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.login_username.insert(0, "Enter your username")
        self.login_username.bind("<FocusIn>", lambda e: self.on_entry_focus(self.login_username, "username"))
        self.login_username.bind("<FocusOut>", lambda e: self.on_entry_blur(self.login_username, "username"))

        # Password field
        tk.Label(
            self.content_frame,
            text="Password",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(anchor=tk.W, padx=0, pady=(0, 5))

        password_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        password_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(password_frame, text="🔒", font=("Helvetica", 12),
                 bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.login_password = tk.Entry(
            password_frame,
            font=("Helvetica", 11),
            bg=self.LIGHT_GRAY,
            border=0,
            fg=self.TEXT_COLOR,
            show="*"
        )
        self.login_password.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.login_password.insert(0, "Enter your password")
        self.login_password.bind("<FocusIn>", lambda e: self.on_entry_focus(self.login_password, "password"))
        self.login_password.bind("<FocusOut>", lambda e: self.on_entry_blur(self.login_password, "password"))

        # Role field
        tk.Label(
            self.content_frame,
            text="Role",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(anchor=tk.W, padx=0, pady=(0, 5))

        role_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        role_frame.pack(fill=tk.X, pady=(0, 25))

        tk.Label(role_frame, text="🛡️", font=("Helvetica", 12),
                 bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.login_role = ttk.Combobox(
            role_frame,
            values=["Student", "Admin"],
            state="readonly",
            font=("Helvetica", 11),
            width=25
        )
        self.login_role.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 10))
        self.login_role.set("Student")

        # Login button
        login_submit_btn = tk.Button(
            self.content_frame,
            text="Log In",
            font=("Helvetica", 12, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR,
            command=self.perform_login,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12
        )
        login_submit_btn.pack(fill=tk.X, pady=(0, 15))

        # Separator
        sep_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        sep_frame.pack(fill=tk.X, pady=10)
        tk.Label(sep_frame, text="or", font=("Helvetica", 10),
                 fg=self.ACCENT_GRAY, bg=self.SECONDARY_COLOR).pack()

        # Sign up link
        signup_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        signup_frame.pack(pady=(0, 20))

        tk.Label(signup_frame, text="Don't have an account? ", font=("Helvetica", 10),
                 fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(side=tk.LEFT)

        signup_link = tk.Label(
            signup_frame,
            text="Sign Up",
            font=("Helvetica", 10, "bold"),
            fg=self.PRIMARY_COLOR,
            bg=self.SECONDARY_COLOR,
            cursor="hand2"
        )
        signup_link.pack(side=tk.LEFT)
        signup_link.bind("<Button-1>", lambda e: self.show_signup_form())

    def show_signup_form(self):
        self.current_mode = "signup"
        self.clear_content_frame()

        # Update toggle buttons
        self.login_toggle_btn.configure(fg=self.ACCENT_GRAY, font=("Helvetica", 16))
        self.signup_toggle_btn.configure(fg=self.PRIMARY_COLOR, font=("Helvetica", 16, "bold"))

        # Welcome message
        tk.Label(
            self.content_frame,
            text="Create Account",
            font=("Helvetica", 20, "bold"),
            fg=self.PRIMARY_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(pady=(0, 5))

        tk.Label(
            self.content_frame,
            text="Join our library community",
            font=("Helvetica", 10),
            fg=self.ACCENT_GRAY,
            bg=self.SECONDARY_COLOR
        ).pack(pady=(0, 25))

        # Username field
        tk.Label(
            self.content_frame,
            text="Username",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(anchor=tk.W, padx=0, pady=(0, 5))

        username_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(username_frame, text="👤", font=("Helvetica", 12),
                 bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.signup_username = tk.Entry(
            username_frame,
            font=("Helvetica", 11),
            bg=self.LIGHT_GRAY,
            border=0,
            fg=self.TEXT_COLOR
        )
        self.signup_username.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.signup_username.insert(0, "Enter your username")
        self.signup_username.bind("<FocusIn>", lambda e: self.on_entry_focus(self.signup_username, "username"))
        self.signup_username.bind("<FocusOut>", lambda e: self.on_entry_blur(self.signup_username, "username"))

        # Password field
        tk.Label(
            self.content_frame,
            text="Password",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(anchor=tk.W, padx=0, pady=(0, 5))

        password_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        password_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(password_frame, text="🔒", font=("Helvetica", 12),
                 bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.signup_password = tk.Entry(
            password_frame,
            font=("Helvetica", 11),
            bg=self.LIGHT_GRAY,
            border=0,
            fg=self.TEXT_COLOR,
            show="*"
        )
        self.signup_password.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.signup_password.insert(0, "Enter your password")
        self.signup_password.bind("<FocusIn>", lambda e: self.on_entry_focus(self.signup_password, "password"))
        self.signup_password.bind("<FocusOut>", lambda e: self.on_entry_blur(self.signup_password, "password"))

        # Confirm Password field
        tk.Label(
            self.content_frame,
            text="Confirm Password",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(anchor=tk.W, padx=0, pady=(0, 5))

        confirm_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        confirm_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(confirm_frame, text="🔒", font=("Helvetica", 12),
                 bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.signup_confirm = tk.Entry(
            confirm_frame,
            font=("Helvetica", 11),
            bg=self.LIGHT_GRAY,
            border=0,
            fg=self.TEXT_COLOR,
            show="*"
        )
        self.signup_confirm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.signup_confirm.insert(0, "Confirm your password")
        self.signup_confirm.bind("<FocusIn>", lambda e: self.on_entry_focus(self.signup_confirm, "confirm"))
        self.signup_confirm.bind("<FocusOut>", lambda e: self.on_entry_blur(self.signup_confirm, "confirm"))

        # Role field
        tk.Label(
            self.content_frame,
            text="Role",
            font=("Helvetica", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.SECONDARY_COLOR
        ).pack(anchor=tk.W, padx=0, pady=(0, 5))

        role_frame = tk.Frame(self.content_frame, bg=self.LIGHT_GRAY, relief=tk.FLAT, bd=1)
        role_frame.pack(fill=tk.X, pady=(0, 25))

        tk.Label(role_frame, text="🛡️", font=("Helvetica", 12),
                 bg=self.LIGHT_GRAY, fg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=10)

        self.signup_role = ttk.Combobox(
            role_frame,
            values=["Student", "Admin"],
            state="readonly",
            font=("Helvetica", 11),
            width=25
        )
        self.signup_role.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=(0, 10))
        self.signup_role.set("Student")

        # Signup button
        signup_submit_btn = tk.Button(
            self.content_frame,
            text="Sign Up",
            font=("Helvetica", 12, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.SECONDARY_COLOR,
            command=self.perform_signup,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12
        )
        signup_submit_btn.pack(fill=tk.X, pady=(0, 15))

        # Separator
        sep_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        sep_frame.pack(fill=tk.X, pady=10)
        tk.Label(sep_frame, text="or", font=("Helvetica", 10),
                 fg=self.ACCENT_GRAY, bg=self.SECONDARY_COLOR).pack()

        # Login link
        login_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        login_frame.pack(pady=(0, 20))

        tk.Label(login_frame, text="Already have an account? ", font=("Helvetica", 10),
                 fg=self.TEXT_COLOR, bg=self.SECONDARY_COLOR).pack(side=tk.LEFT)

        login_link = tk.Label(
            login_frame,
            text="Log In",
            font=("Helvetica", 10, "bold"),
            fg=self.PRIMARY_COLOR,
            bg=self.SECONDARY_COLOR,
            cursor="hand2"
        )
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

        # Placeholder checks
        if username == "Enter your username" or not username:
            messagebox.showerror("Error", "Please enter your username")
            return

        if password == "Enter your password" or not password:
            messagebox.showerror("Error", "Please enter your password")
            return

        if not role:
            messagebox.showerror("Error", "Please select a role")
            return

        # Authenticate
        user = self.db_manager.authenticate_user(username, password)

        if not user:
            messagebox.showerror("Error", "Invalid username or password")
            return

        if user['role'] != role:
            messagebox.showerror("Error", f"This account is registered as {user['role']}")
            return

        # Success
        messagebox.showinfo("Success", f"Welcome {username}!")
        self.on_login_callback(user)

    def perform_signup(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()
        confirm = self.signup_confirm.get().strip()
        role = self.signup_role.get()

        # Placeholder checks
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

        # Check if user exists
        existing_user = self.db_manager.get_user_by_username(username)
        if existing_user:
            messagebox.showerror("Error", "Username already exists")
            return

        # Register user
        try:
            self.db_manager.register_user(username, password, role)
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.show_login_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))