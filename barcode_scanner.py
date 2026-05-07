import threading
import cv2
import numpy as np
from pyzbar.pyzbar import decode

class BarcodeScannerWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.scan_thread = threading.Thread(target=self.run_scanner)
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def run_scanner(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        scanned_isbn = None

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            barcodes = decode(gray_frame)

            for barcode in barcodes:
                raw_data = barcode.data.decode('utf-8')
                clean_data = raw_data.replace("-", "")

                if len(clean_data) == 13 or len(clean_data) == 10:
                    scanned_isbn = clean_data
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    break
                else:
                    continue

            cv2.imshow("Barcode Scanner - Press 'Q' or 'ESC' to Cancel", frame)
            key = cv2.waitKey(1) & 0xFF
            if scanned_isbn or key == ord('q') or key == 27:
                break

            if cv2.getWindowProperty("Barcode Scanner - Press 'Q' or 'ESC' to Cancel", cv2.WND_PROP_VISIBLE) < 1:
                break

        cap.release()
        cv2.destroyAllWindows()
        result = scanned_isbn if scanned_isbn else "X"

        def deliver():
            self.callback(result)

        self.parent.after(0, deliver)