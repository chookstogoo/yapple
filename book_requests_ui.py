import customtkinter as ctk
import book_requests_db as db

# Theme setup to match your screenshot
ctk.set_appearance_mode("dark")


class BookRequestSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Request System Module")
        self.geometry("900x600")

        # Test User ID
        self.current_user = "nikkko"

        # Top Navigation
        self.header = ctk.CTkFrame(self, fg_color="#D92139", height=50, corner_radius=0)
        self.header.pack(fill="x")
        self.header_label = ctk.CTkLabel(self.header, text="Test Environment: Request & Approve", text_color="white",
                                         font=("Arial", 20, "bold"))
        self.header_label.pack(pady=10, padx=20, side="left")

        # Main Tabview
        self.tabview = ctk.CTkTabview(self, fg_color="#2b2b2b")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_user = self.tabview.add("User: Request Books")
        self.tab_user_transactions = self.tabview.add("User: My Transactions")
        self.tab_admin = self.tabview.add("Admin: Pending Requests")

        self.cart = []
        self.setup_user_request_tab()
        self.setup_user_transactions_tab()
        self.setup_admin_tab()

    # ==========================
    # USER: REQUEST BOOKS TAB
    # ==========================
    def setup_user_request_tab(self):
        controls_frame = ctk.CTkFrame(self.tab_user, fg_color="transparent")
        controls_frame.pack(pady=10)

        # Get books from DB for the dropdown
        self.available_books = db.get_all_books()
        book_titles = [book[1] for book in self.available_books]

        self.book_combo = ctk.CTkComboBox(controls_frame, values=book_titles, width=300)
        self.book_combo.grid(row=0, column=0, padx=10)

        self.qty_entry = ctk.CTkEntry(controls_frame, placeholder_text="Qty", width=60)
        self.qty_entry.grid(row=0, column=1, padx=10)

        self.add_btn = ctk.CTkButton(controls_frame, text="Add to Cart", fg_color="#D92139", hover_color="#b31b2e",
                                     command=self.add_to_cart)
        self.add_btn.grid(row=0, column=2, padx=10)

        self.cart_display = ctk.CTkTextbox(self.tab_user, width=500, height=200)
        self.cart_display.pack(pady=10)

        self.submit_btn = ctk.CTkButton(self.tab_user, text="Submit Request to Admin", fg_color="#D92139",
                                        hover_color="#b31b2e", command=self.submit_request)
        self.submit_btn.pack(pady=10)

    def add_to_cart(self):
        title = self.book_combo.get()
        qty = self.qty_entry.get()

        if not qty.isdigit() or int(qty) <= 0:
            return

        # Find Book ID
        book_id = next(book[0] for book in self.available_books if book[1] == title)

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
        self.admin_display = ctk.CTkTextbox(self.tab_admin, width=700, height=250)
        self.admin_display.pack(pady=10)

        controls_frame = ctk.CTkFrame(self.tab_admin, fg_color="transparent")
        controls_frame.pack(pady=10)

        self.approve_id_entry = ctk.CTkEntry(controls_frame, placeholder_text="Enter Transaction ID to Approve",
                                             width=250)
        self.approve_id_entry.grid(row=0, column=0, padx=10)

        self.approve_btn = ctk.CTkButton(controls_frame, text="Approve Request", fg_color="#D92139",
                                         hover_color="#b31b2e", command=self.approve_request)
        self.approve_btn.grid(row=0, column=1, padx=10)

        self.refresh_admin_tab()

    def refresh_admin_tab(self):
        self.admin_display.delete("1.0", "end")
        pending = db.get_pending_requests()

        if not pending:
            self.admin_display.insert("end", "No pending requests.")
            return

        self.admin_display.insert("end", "ID | User | Book Title | Qty | Date\n")
        self.admin_display.insert("end", "-" * 60 + "\n")
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
        self.trans_display = ctk.CTkTextbox(self.tab_user_transactions, width=700, height=250)
        self.trans_display.pack(pady=10)

        controls_frame = ctk.CTkFrame(self.tab_user_transactions, fg_color="transparent")
        controls_frame.pack(pady=10)

        self.return_id_entry = ctk.CTkEntry(controls_frame, placeholder_text="Enter Transaction ID to Return",
                                            width=250)
        self.return_id_entry.grid(row=0, column=0, padx=10)

        self.return_btn = ctk.CTkButton(controls_frame, text="Return Book", fg_color="#D92139", hover_color="#b31b2e",
                                        command=self.return_book)
        self.return_btn.grid(row=0, column=1, padx=10)

        self.refresh_user_transactions()

    def refresh_user_transactions(self):
        self.trans_display.delete("1.0", "end")
        active = db.get_active_transactions(self.current_user)

        if not active:
            self.trans_display.insert("end", "You have no active checkouts.")
            return

        self.trans_display.insert("end", "Active Checkouts:\n")
        self.trans_display.insert("end", "ID | Book Title | Qty | Date Checked Out\n")
        self.trans_display.insert("end", "-" * 60 + "\n")
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