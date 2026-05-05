import tkinter as tk
from tkinter import ttk, messagebox
import book_requests_db as db


class BookRequestSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Request System Module")
        self.geometry("900x600")

        # Test User ID
        self.current_user = "nikkko"

        # Top Navigation
        self.header = tk.Frame(self, bg="#D92139", height=50)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)  # Prevents the frame from shrinking around the label

        self.header_label = tk.Label(self.header, text="Test Environment: Request & Approve",
                                     bg="#D92139", fg="white", font=("Arial", 20, "bold"))
        self.header_label.pack(pady=10, padx=20, side="left")

        # Main Tabview using ttk.Notebook
        self.tabview = ttk.Notebook(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_user = ttk.Frame(self.tabview)
        self.tab_user_transactions = ttk.Frame(self.tabview)
        self.tab_admin = ttk.Frame(self.tabview)

        self.tabview.add(self.tab_user, text="User: Request Books")
        self.tabview.add(self.tab_user_transactions, text="User: My Transactions")
        self.tabview.add(self.tab_admin, text="Admin: Pending Requests")

        self.cart = []
        self.setup_user_request_tab()
        self.setup_user_transactions_tab()
        self.setup_admin_tab()

    # ==========================
    # USER: REQUEST BOOKS TAB
    # ==========================
    def setup_user_request_tab(self):
        controls_frame = tk.Frame(self.tab_user)
        controls_frame.pack(pady=10)

        # Get books from DB for the dropdown
        self.available_books = db.get_all_books()
        book_titles = [book[1] for book in self.available_books] if self.available_books else []

        self.book_combo = ttk.Combobox(controls_frame, values=book_titles, width=40, state="readonly")
        self.book_combo.grid(row=0, column=0, padx=10)
        if book_titles:
            self.book_combo.current(0)  # Select first item by default

        # Standard Tkinter Entry with manual placeholder logic
        self.qty_entry = tk.Entry(controls_frame, width=10)
        self.qty_entry.insert(0, "Qty")

        def clear_qty_placeholder(e):
            if self.qty_entry.get() == "Qty":
                self.qty_entry.delete(0, "end")

        self.qty_entry.bind("<FocusIn>", clear_qty_placeholder)
        self.qty_entry.grid(row=0, column=1, padx=10)

        self.add_btn = tk.Button(controls_frame, text="Add to Cart", bg="#D92139", fg="white",
                                 command=self.add_to_cart, relief="flat", padx=10, pady=2)
        self.add_btn.grid(row=0, column=2, padx=10)

        self.cart_display = tk.Text(self.tab_user, width=70, height=12)
        self.cart_display.pack(pady=10)

        self.submit_btn = tk.Button(self.tab_user, text="Submit Request to Admin", bg="#D92139", fg="white",
                                    command=self.submit_request, relief="flat", padx=15, pady=5)
        self.submit_btn.pack(pady=10)

    def add_to_cart(self):
        title = self.book_combo.get()
        qty = self.qty_entry.get()

        if not qty.isdigit() or int(qty) <= 0:
            return

        # Find Book ID safely
        try:
            book_id = next(book[0] for book in self.available_books if book[1] == title)
        except StopIteration:
            return

        self.cart.append({'book_id': book_id, 'title': title, 'qty': int(qty)})
        self.cart_display.insert("end", f"Added: {title} (Quantity: {qty})\n")
        self.qty_entry.delete(0, 'end')

    def submit_request(self):
        if self.cart:
            db.request_books(self.current_user, self.cart)
            self.cart.clear()
            self.cart_display.delete("1.0", "end")
            self.cart_display.insert("end", "✅ Request submitted successfully! Waiting for Admin approval.\n")
            self.refresh_admin_tab()  # Auto-refresh admin view for testing

    # ==========================
    # ADMIN: PENDING REQUESTS
    # ==========================
    def setup_admin_tab(self):
        self.admin_display = tk.Text(self.tab_admin, width=85, height=15)
        self.admin_display.pack(pady=10)

        controls_frame = tk.Frame(self.tab_admin)
        controls_frame.pack(pady=10)

        self.approve_id_entry = tk.Entry(controls_frame, width=35)
        self.approve_id_entry.insert(0, "Enter Transaction ID to Approve")

        def clear_approve_placeholder(e):
            if self.approve_id_entry.get() == "Enter Transaction ID to Approve":
                self.approve_id_entry.delete(0, "end")

        self.approve_id_entry.bind("<FocusIn>", clear_approve_placeholder)
        self.approve_id_entry.grid(row=0, column=0, padx=10)

        self.approve_btn = tk.Button(controls_frame, text="Approve Request", bg="#D92139", fg="white",
                                     command=self.approve_request, relief="flat", padx=10, pady=2)
        self.approve_btn.grid(row=0, column=1, padx=10)

        self.refresh_admin_tab()

    def refresh_admin_tab(self):
        self.admin_display.delete("1.0", "end")
        pending = db.get_pending_requests()

        if not pending:
            self.admin_display.insert("end", "No pending requests.")
            self.pending_requests_data = []
            return

        self.admin_display.insert("end", "ID | User | Book Title | Qty | Date\n")
        self.admin_display.insert("end", "-" * 75 + "\n")
        for req in pending:
            self.admin_display.insert("end", f"[{req[0]}] {req[1]} requested {req[3]}x '{req[2]}' on {req[4]}\n")

        # Store for reference
        self.pending_requests_data = pending

    def approve_request(self):
        trans_id = self.approve_id_entry.get()
        if not trans_id.isdigit(): return
        trans_id = int(trans_id)

        # Find the matching request to get all data needed for approval
        req = next((r for r in self.pending_requests_data if r[0] == trans_id), None)

        if req:
            db.admin_approve_request(transaction_id=req[0], user_id=req[1], book_id=req[5], quantity=req[3])
            self.approve_id_entry.delete(0, 'end')
            self.refresh_admin_tab()
            self.refresh_user_transactions()  # Auto-refresh user view

    # ==========================
    # USER: MY TRANSACTIONS
    # ==========================
    def setup_user_transactions_tab(self):
        self.trans_display = tk.Text(self.tab_user_transactions, width=85, height=15)
        self.trans_display.pack(pady=10)

        controls_frame = tk.Frame(self.tab_user_transactions)
        controls_frame.pack(pady=10)

        self.return_id_entry = tk.Entry(controls_frame, width=35)
        self.return_id_entry.insert(0, "Enter Transaction ID to Return")

        def clear_return_placeholder(e):
            if self.return_id_entry.get() == "Enter Transaction ID to Return":
                self.return_id_entry.delete(0, "end")

        self.return_id_entry.bind("<FocusIn>", clear_return_placeholder)
        self.return_id_entry.grid(row=0, column=0, padx=10)

        self.return_btn = tk.Button(controls_frame, text="Return Book", bg="#D92139", fg="white",
                                    command=self.return_book, relief="flat", padx=10, pady=2)
        self.return_btn.grid(row=0, column=1, padx=10)

        self.refresh_user_transactions()

    def refresh_user_transactions(self):
        self.trans_display.delete("1.0", "end")
        active = db.get_active_transactions(self.current_user)

        if not active:
            self.trans_display.insert("end", "You have no active checkouts.")
            self.active_transactions_data = []
            return

        self.trans_display.insert("end", "Active Checkouts:\n")
        self.trans_display.insert("end", "ID | Book Title | Qty | Date Checked Out\n")
        self.trans_display.insert("end", "-" * 75 + "\n")
        for act in active:
            self.trans_display.insert("end", f"[{act[0]}] {act[1]} (Qty: {act[2]}) - {act[3]}\n")

        self.active_transactions_data = active

    def return_book(self):
        trans_id = self.return_id_entry.get()
        if not trans_id.isdigit(): return
        trans_id = int(trans_id)

        act = next((a for a in self.active_transactions_data if a[0] == trans_id), None)

        if act:
            db.return_book(transaction_id=act[0], book_id=act[4], quantity=act[2])
            self.return_id_entry.delete(0, 'end')
            self.refresh_user_transactions()


if __name__ == "__main__":
    app = BookRequestSystem()
    app.mainloop()