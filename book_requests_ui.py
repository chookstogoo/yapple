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
        self.header.pack_propagate(False)

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

        self.available_books = db.get_all_books()
        book_titles = [book[1] if isinstance(book, tuple) else book.get('title') for book in
                       self.available_books] if self.available_books else []

        self.book_combo = ttk.Combobox(controls_frame, values=book_titles, width=40, state="readonly")
        self.book_combo.grid(row=0, column=0, padx=10)
        if book_titles:
            self.book_combo.current(0)

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

        # Hard block typing and pasting, without touching the submit_request method below
        self.cart_display.bind("<Key>", lambda e: "break")
        self.cart_display.bind("<Button-2>", lambda e: "break")
        self.cart_display.bind("<Button-3>", lambda e: "break")

        self.submit_btn = tk.Button(self.tab_user, text="Submit Request to Admin", bg="#D92139", fg="white",
                                    command=self.submit_request, relief="flat", padx=15, pady=5)
        self.submit_btn.pack(pady=10)

    def add_to_cart(self):
        title = self.book_combo.get()
        qty = self.qty_entry.get()

        if not qty.isdigit() or int(qty) <= 0:
            return

        try:
            # Handle tuple or dict safely
            book_id = next((b[0] if isinstance(b, tuple) else b.get('book_id')) for b in self.available_books if
                           (b[1] if isinstance(b, tuple) else b.get('title')) == title)
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
        # UPGRADE: Replaced tk.Text with ttk.Treeview to fix barcode/quantity layout & enable double-clicking
        columns = ("ID", "User", "Title", "Qty", "Date", "Barcode")
        self.admin_tree = ttk.Treeview(self.tab_admin, columns=columns, show="headings", height=8)

        for col in columns:
            self.admin_tree.heading(col, text=col)

        self.admin_tree.column("ID", width=50)
        self.admin_tree.column("User", width=80)
        self.admin_tree.column("Title", width=250)
        self.admin_tree.column("Qty", width=50)
        self.admin_tree.column("Date", width=150)
        self.admin_tree.column("Barcode", width=120)
        self.admin_tree.pack(pady=10, fill="x", padx=20)

        # Allow Double Clicking!
        self.admin_tree.bind("<Double-1>", self.on_admin_double_click)

        controls_frame = tk.Frame(self.tab_admin)
        controls_frame.pack(pady=10)

        # Approve Section
        self.approve_id_entry = tk.Entry(controls_frame, width=35)
        self.approve_id_entry.insert(0, "Enter Transaction ID to Approve")
        self.approve_id_entry.bind("<FocusIn>", lambda e: self.approve_id_entry.delete(0,
                                                                                       "end") if self.approve_id_entry.get() == "Enter Transaction ID to Approve" else None)
        self.approve_id_entry.grid(row=0, column=0, padx=10, pady=5)

        self.approve_btn = tk.Button(controls_frame, text="Approve Request", bg="#D92139", fg="white",
                                     command=self.approve_request, relief="flat", padx=10, pady=2)
        self.approve_btn.grid(row=0, column=1, padx=10, pady=5)

        # Reject Section
        self.reject_id_entry = tk.Entry(controls_frame, width=35)
        self.reject_id_entry.insert(0, "Enter Transaction ID to Reject")
        self.reject_id_entry.bind("<FocusIn>", lambda e: self.reject_id_entry.delete(0,
                                                                                     "end") if self.reject_id_entry.get() == "Enter Transaction ID to Reject" else None)
        self.reject_id_entry.grid(row=1, column=0, padx=10, pady=5)

        self.reject_btn = tk.Button(controls_frame, text="Reject Request", bg="#DC3545", fg="white",
                                    command=self.reject_request, relief="flat", padx=10, pady=2)
        self.reject_btn.grid(row=1, column=1, padx=10, pady=5)

        self.refresh_admin_tab()

    def on_admin_double_click(self, event):
        selected = self.admin_tree.selection()
        if selected:
            item = self.admin_tree.item(selected[0])
            req_id = item['values'][0]
            # Auto fill both entries
            self.approve_id_entry.delete(0, 'end')
            self.approve_id_entry.insert(0, str(req_id))
            self.reject_id_entry.delete(0, 'end')
            self.reject_id_entry.insert(0, str(req_id))

    def refresh_admin_tab(self):
        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)

        pending = db.get_pending_requests()
        self.pending_requests_data = pending or []

        if not pending:
            return

        for req in pending:
            # Safely fetch keys whether it's a dict or a tuple
            if isinstance(req, dict):
                self.admin_tree.insert("", "end", values=(
                    req.get('transaction_id'), req.get('username'), req.get('title'),
                    req.get('qty_requested'), req.get('transaction_date'), req.get('barcode', 'N/A')
                ))
            else:
                barcode = req[7] if len(req) > 7 else "N/A"
                self.admin_tree.insert("", "end", values=(req[0], req[3], req[4], req[5], req[6], barcode))

    def approve_request(self):
        trans_id = self.approve_id_entry.get()
        if not trans_id.isdigit(): return
        trans_id = int(trans_id)

        # Dictionary safe indexing
        def get_id(r):
            return r.get('transaction_id') if isinstance(r, dict) else r[0]

        req = next((r for r in self.pending_requests_data if get_id(r) == trans_id), None)

        if req:
            u_id = req.get('user_id') if isinstance(req, dict) else req[1]
            b_id = req.get('book_id') if isinstance(req, dict) else req[2]
            qty = req.get('qty_requested') if isinstance(req, dict) else req[5]

            db.admin_approve_request(transaction_id=trans_id, user_id=u_id, book_id=b_id, quantity=qty)
            self.approve_id_entry.delete(0, 'end')
            self.refresh_admin_tab()
            self.refresh_user_transactions()

    def reject_request(self):
        trans_id = self.reject_id_entry.get()
        if not trans_id.isdigit(): return
        trans_id = int(trans_id)

        def get_id(r):
            return r.get('transaction_id') if isinstance(r, dict) else r[0]

        req = next((r for r in self.pending_requests_data if get_id(r) == trans_id), None)

        if req:
            # FIX: Used proper DB method instead of buggy inline sqlite code (`WHERE id = ?` -> `transaction_id = ?`)
            try:
                db.update_request_status(trans_id, 'Rejected')
            except Exception:
                pass  # Just in case connection drops

            self.reject_id_entry.delete(0, 'end')
            self.refresh_admin_tab()

    # ==========================
    # USER: MY TRANSACTIONS
    # ==========================
    def setup_user_transactions_tab(self):
        # UPGRADE: Replaced tk.Text with ttk.Treeview to fix quantity display and prevent typing
        columns = ("ID", "Title", "Qty", "Date", "Status")
        self.trans_tree = ttk.Treeview(self.tab_user_transactions, columns=columns, show="headings", height=8)

        for col in columns:
            self.trans_tree.heading(col, text=col)

        self.trans_tree.column("ID", width=50)
        self.trans_tree.column("Title", width=300)
        self.trans_tree.column("Qty", width=50)
        self.trans_tree.column("Date", width=150)
        self.trans_tree.column("Status", width=100)
        self.trans_tree.pack(pady=10, fill="x", padx=20)

        # Adding double click for returning too
        self.trans_tree.bind("<Double-1>", self.on_trans_double_click)

        controls_frame = tk.Frame(self.tab_user_transactions)
        controls_frame.pack(pady=10)

        self.return_id_entry = tk.Entry(controls_frame, width=35)
        self.return_id_entry.insert(0, "Enter Transaction ID to Return")
        self.return_id_entry.bind("<FocusIn>", lambda e: self.return_id_entry.delete(0,
                                                                                     "end") if self.return_id_entry.get() == "Enter Transaction ID to Return" else None)
        self.return_id_entry.grid(row=0, column=0, padx=10)

        self.return_btn = tk.Button(controls_frame, text="Return Book", bg="#D92139", fg="white",
                                    command=self.return_book, relief="flat", padx=10, pady=2)
        self.return_btn.grid(row=0, column=1, padx=10)

        self.refresh_user_transactions()

    def on_trans_double_click(self, event):
        selected = self.trans_tree.selection()
        if selected:
            item = self.trans_tree.item(selected[0])
            req_id = item['values'][0]
            self.return_id_entry.delete(0, 'end')
            self.return_id_entry.insert(0, str(req_id))

    def refresh_user_transactions(self):
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)

        try:
            active = db.get_active_transactions(self.current_user)
        except AttributeError:
            active = []

        self.active_transactions_data = active or []

        if not active:
            return

        for act in active:
            if isinstance(act, dict):
                self.trans_tree.insert("", "end", values=(
                    act.get('transaction_id'), act.get('title'), act.get('quantity'),
                    act.get('transaction_date'), act.get('status', 'Active')
                ))
            else:
                qty = act[7] if len(act) > 7 else act[2]
                status = act[6] if len(act) > 6 else 'Active'
                self.trans_tree.insert("", "end", values=(act[0], act[1], qty, act[3], status))

    def return_book(self):
        trans_id = self.return_id_entry.get()
        if not trans_id.isdigit(): return
        trans_id = int(trans_id)

        def get_id(a):
            return a.get('transaction_id') if isinstance(a, dict) else a[0]

        act = next((a for a in self.active_transactions_data if get_id(a) == trans_id), None)

        if act:
            b_id = act.get('book_id') if isinstance(act, dict) else act[4]
            qty = act.get('quantity') if isinstance(act, dict) else (act[7] if len(act) > 7 else act[2])

            db.return_book(transaction_id=trans_id, book_id=b_id, quantity_str=str(qty))
            self.return_id_entry.delete(0, 'end')
            self.refresh_user_transactions()


if __name__ == "__main__":
    app = BookRequestSystem()
    app.mainloop()