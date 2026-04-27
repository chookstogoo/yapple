import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from barcode_generator import BarcodeGenerator  # Changed import
from PIL import Image, ImageTk
import io
from datetime import datetime


class StudentDashboard:

    def __init__(self, root, user_data, db_manager, logout_callback):
        # ... (keep existing init code) ...

        self.barcode_generator = BarcodeGenerator()  # Replaced QR Generator

        # Configure root window
        self.root.configure(bg=self.DARK_BG)
        self.root.geometry("900x600")
        self.root.minsize(900, 600)

        self.setup_ui()

    # ... (keep all intermediate setup functions the same) ...

    def on_book_selected(self, event):
        selection = self.books_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.books_tree.item(item, 'values')
        book_id, title, author, isbn, available, status = values

        self.show_barcode(int(book_id), title, author, isbn)  # Changed method call

    def show_barcode(self, book_id, title, author, isbn):  # Renamed method
        barcode_window = tk.Toplevel(self.root)
        barcode_window.title("📖 Book Info")
        barcode_window.geometry("380x420")
        barcode_window.configure(bg=self.DARK_BG)
        barcode_window.resizable(False, False)

        # Header
        header = tk.Frame(barcode_window, bg=self.PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text="Book Details & Barcode",  # Changed text
            font=("Segoe UI", 12, "bold"),
            fg=self.SECONDARY_COLOR,
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

        # Barcode section
        barcode_section = tk.Frame(content, bg=self.SECONDARY_COLOR, relief=tk.FLAT, bd=0)
        barcode_section.pack(fill=tk.BOTH, expand=True, pady=8)

        barcode_label = tk.Label(barcode_section, bg=self.SECONDARY_COLOR)
        barcode_label.pack(pady=8)

        try:
            # We use the ISBN for the barcode as it makes the most sense practically
            # and keeps the barcode clean and scannable.
            barcode_image = self.barcode_generator.generate_barcode(str(isbn))

            barcode_photo = ImageTk.PhotoImage(barcode_image)
            barcode_label.config(image=barcode_photo)
            barcode_label.image = barcode_photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate barcode: {str(e)}")

    # ... (keep remaining methods the same) ...