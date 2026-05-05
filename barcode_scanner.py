import threading

import cv2
import numpy as np
from pyzbar.pyzbar import decode

class BarcodeScannerWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback

        # We run the scanner in a separate thread so it doesn't freeze your Tkinter UI
        self.scan_thread = threading.Thread(target=self.run_scanner)
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def run_scanner(self):
        # 1. Open camera with DirectShow for better Windows performance
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # 2. FORCE 1080p (1920x1080)
        # If your webcam only supports 720p, it will automatically scale to its max
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        scanned_isbn = None

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert the frame to grayscale for the decoder (removes visual noise/grain)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Look for barcodes in the CLEAN grayscale frame
            barcodes = decode(gray_frame)

            for barcode in barcodes:
                # Decode the raw barcode data to a string
                raw_data = barcode.data.decode('utf-8')

                # Clean the data just in case it brings in hyphens
                clean_data = raw_data.replace("-", "")

                # FILTER: Only accept standard ISBN lengths (10 or 13 digits)
                if len(clean_data) == 13 or len(clean_data) == 10:
                    scanned_isbn = clean_data

                    # Draw a green box around the detected barcode on the ORIGINAL COLOR frame
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    break  # We found a valid ISBN, stop scanning!
                else:
                    # It's a partial read or a price code. Ignore it and keep looking.
                    continue

            # Display the NORMAL color video feed to the user
            cv2.imshow("Barcode Scanner - Press 'Q' or 'ESC' to Cancel", frame)

            # Check if we successfully scanned something, OR if the user pressed Q/ESC to quit
            key = cv2.waitKey(1) & 0xFF
            if scanned_isbn or key == ord('q') or key == 27:
                break

            # Check if the user clicked the "X" button on the window to close it
            if cv2.getWindowProperty("Barcode Scanner - Press 'Q' or 'ESC' to Cancel", cv2.WND_PROP_VISIBLE) < 1:
                break

        # 4. Clean up the camera resources
        cap.release()
        cv2.destroyAllWindows()

        # 5. Send the result on the Tk main thread (callbacks must not run from this worker thread)
        result = scanned_isbn if scanned_isbn else "X"

        def deliver():
            self.callback(result)

        self.parent.after(0, deliver)