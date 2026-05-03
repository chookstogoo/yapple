import tkinter as tk
from ui import LibraryManagementApp


def main():
    # Initialize the main Tkinter window
    root = tk.Tk()

    # Pass the root window to your consolidated app class
    app = LibraryManagementApp(root)

    # Start the application loop
    root.mainloop()


if __name__ == "__main__":
    main()