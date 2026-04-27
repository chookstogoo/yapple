import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from login_window import LoginWindow
from database import DatabaseManager

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
        role = user_data['role']
        username = user_data['username']
        
        if role == 'Student':
            self.show_student_dashboard(user_data)
        elif role == 'Admin':
            self.show_admin_dashboard(user_data)
    
    def show_student_dashboard(self, user_data):
        from student_dashboard import StudentDashboard
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        dashboard = StudentDashboard(self.root, user_data, self.db_manager, self.show_login_window)
    
    def show_admin_dashboard(self, user_data):
        from admin_dashboard import AdminDashboard
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        dashboard = AdminDashboard(self.root, user_data, self.db_manager, self.show_login_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()