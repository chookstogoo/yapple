import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from PIL import Image, ImageTk


class BarcodeScannerWindow:
    def __init__(self, parent, on_scan_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("📷 Scan Barcode")
        self.top.geometry("640x480")
        self.top.configure(bg="#1E1E1E")
        self.top.resizable(False, False)

        # The function to run when a barcode is found
        self.on_scan_callback = on_scan_callback

        # Open the default webcam (0)
        self.vid = cv2.VideoCapture(0)

        # Canvas to hold the live video stream
        self.canvas = tk.Canvas(self.top, width=640, height=480, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Start the video loop
        self.update_frame()

        # Handle the user clicking the 'X' button gracefully
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        ret, frame = self.vid.read()
        if ret:
            # 1. Look for barcodes in the current frame
            barcodes = decode(frame)
            for barcode in barcodes:
                # We found one! Extract the text
                barcode_data = barcode.data.decode('utf-8')

                # Trigger the callback with the scanned data
                self.on_scan_callback(barcode_data)

                # Cleanup and close the scanner window
                self.on_close()
                return

            # 2. If no barcode, convert the OpenCV frame (BGR) to Tkinter format (RGB)
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv_image)
            self.photo = ImageTk.PhotoImage(image=pil_image)

            # 3. Draw it on the canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Loop this function every 15ms
        self.update_job = self.top.after(15, self.update_frame)

    def on_close(self):
        # Stop the after() loop to prevent errors
        if hasattr(self, 'update_job'):
            self.top.after_cancel(self.update_job)

        # Release the webcam
        if self.vid.isOpened():
            self.vid.release()

        self.top.destroy()