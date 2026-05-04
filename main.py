import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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

        self.PRIMARY_COLOR = "#DC143C"
        self.SECONDARY_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#333333"
        self.LIGHT_GRAY = "#F5F5F5"
        self.ACCENT_GRAY = "#999999"

        try:
            self.original_image = Image.open("image (37).png")
        except FileNotFoundError:
            self.original_image = None
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
            self.image_canvas.create_image(new_width // 2, new_height // 2, anchor=tk.CENTER, image=self.display_image)

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

        tk.Label(title_frame, text="📚", font=("Helvetica", 60), bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR).pack()
        tk.Label(title_frame, text="LIBRARY", font=("Helvetica", 32, "bold"), bg=self.PRIMARY_COLOR,
                 fg=self.SECONDARY_COLOR).pack()

        self.image_canvas = tk.Canvas(sidebar_content, bg=self.PRIMARY_COLOR, highlightthickness=0)
        self.image_canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(20, 0))
        self.image_canvas.bind("<Configure>", self.resize_image)

        right_section = tk.Frame(main_container, bg=self.SECONDARY_COLOR)
        right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.center_container = tk.Frame(right_section, bg=self.SECONDARY_COLOR)
        self.center_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380)

        toggle_frame = tk.Frame(self.center_container, bg=self.SECONDARY_COLOR)
        toggle_frame.pack(fill=tk.X, pady=(0, 30))

        self.login_toggle_btn = tk.Button(toggle_frame, text="Log In", font=("Helvetica", 16, "bold"),
                                          bg=self.SECONDARY_COLOR, fg=self.PRIMARY_COLOR, command=self.show_login_form,
                                          relief=tk.FLAT, bd=0)
        self.login_toggle_btn.pack(side=tk.LEFT)
        tk.Label(toggle_frame, text=" | ", font=("Helvetica", 16), bg=self.SECONDARY_COLOR).pack(side=tk.LEFT)
        self.signup_toggle_btn = tk.Button(toggle_frame, text="Sign Up", font=("Helvetica", 16),
                                           bg=self.SECONDARY_COLOR, fg=self.ACCENT_GRAY, command=self.show_signup_form,
                                           relief=tk.FLAT, bd=0)
        self.signup_toggle_btn.pack(side=tk.LEFT)

        self.content_frame = tk.Frame(self.center_container, bg=self.SECONDARY_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=False)
        self.show_login_form()

    def show_login_form(self):
        for widget in self.content_frame.winfo_children(): widget.destroy()

        self.login_username = tk.Entry(self.content_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY)
        self.login_username.pack(fill=tk.X, pady=10)
        self.login_username.insert(0, "Username")

        self.login_password = tk.Entry(self.content_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY, show="*")
        self.login_password.pack(fill=tk.X, pady=10)

        self.login_role = ttk.Combobox(self.content_frame, values=["Student", "Admin"], state="readonly")
        self.login_role.pack(fill=tk.X, pady=10)
        self.login_role.set("Student")

        tk.Button(self.content_frame, text="Log In", font=("Helvetica", 12, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=self.perform_login).pack(fill=tk.X, pady=15)

    def show_signup_form(self):
        for widget in self.content_frame.winfo_children(): widget.destroy()

        self.signup_username = tk.Entry(self.content_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY)
        self.signup_username.pack(fill=tk.X, pady=10)

        self.signup_password = tk.Entry(self.content_frame, font=("Helvetica", 11), bg=self.LIGHT_GRAY, show="*")
        self.signup_password.pack(fill=tk.X, pady=10)

        self.signup_role = ttk.Combobox(self.content_frame, values=["Student", "Admin"], state="readonly")
        self.signup_role.pack(fill=tk.X, pady=10)
        self.signup_role.set("Student")

        tk.Button(self.content_frame, text="Sign Up", font=("Helvetica", 12, "bold"), bg=self.PRIMARY_COLOR,
                  fg=self.SECONDARY_COLOR, command=self.perform_signup).pack(fill=tk.X, pady=15)

    def perform_login(self):
        user = self.db_manager.authenticate_user(self.login_username.get(), self.login_password.get())
        if not user or user['role'] != self.login_role.get():
            messagebox.showerror("Error", "Invalid credentials or role.")
            return
        self.on_login_callback(user)

    def perform_signup(self):
        try:
            self.db_manager.register_user(self.signup_username.get(), self.signup_password.get(),
                                          self.signup_role.get())
            messagebox.showinfo("Success", "Account created!")
            self.show_login_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class AdminDashboard:
    def __init__(self, root, user_data, db_manager, logout_callback):
        self.root, self.user_data, self.db_manager, self.logout_callback = root, user_data, db_manager, logout_callback
        self.PRIMARY_COLOR, self.SECONDARY_COLOR, self.ACCENT_COLOR = "#DC143C", "#FFFFFF", "#F5F5F5"
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg=self.SECONDARY_COLOR)
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"👨‍💼 Welcome, {self.user_data['username']}! (Admin)", font=("Helvetica", 16, "bold"),
                 fg=self.SECONDARY_COLOR, bg=self.PRIMARY_COLOR).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(header, text="LOGOUT", font=("Helvetica", 10, "bold"), bg=self.SECONDARY_COLOR, fg=self.PRIMARY_COLOR,
                  command=self.logout_callback).pack(side=tk.RIGHT, padx=20, pady=20)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.book_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.book_tab, text="📚 Book Management")
        self.setup_book_management_tab()

        # NEW TAB: Pending Requests
        self.pending_tab = tk.Frame(notebook, bg=self.SECONDARY_COLOR)
        notebook.add(self.pending_tab, text="⏳ Pending Requests")
        self.setup_pending_tab()

    def setup_book_management_tab(self):
        btn_frame = tk.Frame(self.book_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        btn_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(btn_frame, text="🔄 REFRESH", bg="#28A745", fg=self.SECONDARY_COLOR, command=self.load_books).pack(
            side=tk.LEFT, padx=5)

        columns = ("ID", "Title", "Author", "ISBN", "Total", "Available")
        self.books_tree = ttk.Treeview(self.book_tab, columns=columns, height=15, show="headings")
        for col in columns: self.books_tree.heading(col, text=col)
        self.books_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.load_books()

    def load_books(self):
        for i in self.books_tree.get_children(): self.books_tree.delete(i)
        for b in self.db_manager.get_all_books():
            self.books_tree.insert('', tk.END, values=(b['book_id'], b['title'], b['author'], b['isbn'], b['quantity'],
                                                       b['available_quantity']))

    def setup_pending_tab(self):
        btn_frame = tk.Frame(self.pending_tab, bg=self.ACCENT_COLOR, relief=tk.RAISED, bd=2)
        btn_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Button(btn_frame, text="✅ APPROVE SELECTED", bg="#28A745", fg=self.SECONDARY_COLOR,
                  command=self.approve_request).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 REFRESH", bg=self.PRIMARY_COLOR, fg=self.SECONDARY_COLOR,
                  command=self.load_pending).pack(side=tk.LEFT, padx=5)

        cols = ("Trans ID", "User", "Book Title", "Qty Requested", "Date")
        self.pending_tree = ttk.Treeview(self.pending_tab, columns=cols, height=15, show="headings")
        for col in cols: self.pending_tree.heading(col, text=col)
        self.pending_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.load_pending()

    def load_pending(self):
        for i in self.pending_tree.get_children(): self.pending_tree.delete(i)
        for r in self.db_manager.get_pending_requests():
            self.pending_tree.insert('', tk.END,
                                     values=(r['transaction_id'], r['username'], r['title'], r['qty_requested'],
                                             r['transaction_date']))

    def approve_request(self):
        selection = self.pending_tree.selection()
        if not selection: return messagebox.showwarning("Warning", "Select a request.")

        trans_id = self.pending_tree.item(selection[0], 'values')[0]
        reqs = self.db_manager.get_pending_requests()
        req = next((r for r in reqs if str(r['transaction_id']) == str(trans_id)), None)

        if req:
            self.db_manager.admin_approve_request(req['transaction_id'], req['user_id'], req['book_id'],
                                                  req['qty_requested'])
            messagebox.showinfo("Success", "Request Approved!")
            self.load_pending()
            self.load_books()


class StudentDashboard:
    def __init__(self, root, user_data, db_manager, logout_callback):
        self.root, self.user_data, self.db_manager, self.logout_callback = root, user_data, db_manager, logout_callback
        self.DARK_BG, self.PRIMARY_COLOR, self.TEXT_COLOR = "#1E1E1E", "#DC143C", "#FFFFFF"
        self.cart = []
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg=self.DARK_BG)
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"Welcome, {self.user_data['username']}!", bg=self.PRIMARY_COLOR, fg=self.TEXT_COLOR,
                 font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Button(header, text="Logout", bg="#2D2D2D", fg=self.TEXT_COLOR, command=self.logout_callback).pack(
            side=tk.RIGHT, padx=20)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Tab 1: Request Books & Returns
        self.request_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(self.request_frame, text="Request Books & Returns")
        self.setup_request_tab()

        # Tab 2: Transactions / Library
        self.trans_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(self.trans_frame, text="My Transactions")
        self.setup_trans_tab()

    def setup_request_tab(self):
        tk.Label(self.request_frame, text="1. Select Books for Request", bg=self.DARK_BG, fg=self.TEXT_COLOR,
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))

        top_frame = tk.Frame(self.request_frame, bg=self.DARK_BG)
        top_frame.pack(fill=tk.X, padx=10)

        self.book_combo = ttk.Combobox(top_frame, state="readonly", width=40)
        self.book_combo.pack(side=tk.LEFT, padx=5)

        self.qty_entry = tk.Entry(top_frame, width=10)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Add to Request", bg=self.PRIMARY_COLOR, fg=self.TEXT_COLOR,
                  command=self.add_to_cart).pack(side=tk.LEFT, padx=5)

        self.cart_text = tk.Text(self.request_frame, height=6, bg="#2D2D2D", fg=self.TEXT_COLOR)
        self.cart_text.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(self.request_frame, text="Submit Request", bg=self.PRIMARY_COLOR, fg=self.TEXT_COLOR,
                  command=self.submit_request).pack(pady=5)

        # Return Section inside the same tab
        tk.Label(self.request_frame, text="2. Return a Borrowed Book", bg=self.DARK_BG, fg=self.TEXT_COLOR,
                 font=("Segoe UI", 12, "bold")).pack(pady=(20, 5))
        ret_frame = tk.Frame(self.request_frame, bg=self.DARK_BG)
        ret_frame.pack(fill=tk.X, padx=10)

        self.return_combo = ttk.Combobox(ret_frame, state="readonly", width=50)
        self.return_combo.pack(side=tk.LEFT, padx=5)
        tk.Button(ret_frame, text="Return Selected", bg="#28A745", fg=self.TEXT_COLOR,
                  command=self.process_return).pack(side=tk.LEFT, padx=5)

        self.refresh_combos()

    def refresh_combos(self):
        # Update Request Combo
        self.avail_data = self.db_manager.get_all_books()
        self.book_combo['values'] = [f"[{b['book_id']}] {b['title']} (Avail: {b['available_quantity']})" for b in
                                     self.avail_data]

        # Update Return Combo
        self.borrow_data = self.db_manager.get_user_borrowed_books(self.user_data['user_id'])
        self.return_combo['values'] = [f"Trans ID: {t['transaction_id']} | {t['title']} (Qty: {t['transaction_type']})"
                                       for t in self.borrow_data]

    def add_to_cart(self):
        sel = self.book_combo.get()
        qty = self.qty_entry.get()
        if not sel or not qty.isdigit(): return

        book_id = int(sel.split(']')[0].replace('[', ''))
        title = sel.split('] ')[1].split(' (Avail:')[0]

        self.cart.append({'book_id': book_id, 'title': title, 'qty': int(qty)})
        self.cart_text.insert(tk.END, f"{title} - Qty: {qty}\n")

    def submit_request(self):
        if not self.cart: return
        self.db_manager.request_books(self.user_data['user_id'], self.cart)
        self.cart.clear()
        self.cart_text.delete(1.0, tk.END)
        messagebox.showinfo("Success", "Requests pending admin approval!")
        self.load_transactions()

    def process_return(self):
        sel = self.return_combo.get()
        if not sel: return

        trans_id = int(sel.split(' |')[0].replace('Trans ID: ', ''))
        t = next((x for x in self.borrow_data if x['transaction_id'] == trans_id), None)

        if t:
            self.db_manager.return_book(trans_id, t['book_id'], t['transaction_type'])
            messagebox.showinfo("Success", "Book returned!")
            self.refresh_combos()
            self.load_transactions()

    def setup_trans_tab(self):
        cols = ('Title', 'Borrowed Date', 'Due Date')
        self.trans_tree = ttk.Treeview(self.trans_frame, columns=cols, show='headings')
        for col in cols: self.trans_tree.heading(col, text=col)
        self.trans_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)
        self.load_transactions()

    def load_transactions(self):
        for i in self.trans_tree.get_children(): self.trans_tree.delete(i)
        for t in self.db_manager.get_user_borrowed_books(self.user_data['user_id']):
            self.trans_tree.insert('', tk.END, values=(t['title'], t['transaction_date'][:16], t['due_date'][:16]))


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

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()