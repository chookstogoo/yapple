import qrcode
from io import BytesIO
from PIL import Image
import os


class QRCodeGenerator:
    """QR Code generator for books - Encapsulation principle"""

    def __init__(self):
        self.version = 1
        self.box_size = 10
        self.border = 4

    def generate_qr(self, data):
        """Generate QR code from data and return PIL Image"""
        try:
            if not data or not isinstance(data, str):
                raise ValueError("Data must be a non-empty string")

            qr = qrcode.QRCode(
                version=self.version,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=self.box_size,
                border=self.border,
            )

            qr.add_data(data)
            qr.make(fit=True)

            # Create image with red and white colors
            img = qr.make_image(fill_color="#DC143C", back_color="#FFFFFF")

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize for display
            img = img.resize((300, 300), Image.Resampling.LANCZOS)

            return img
        except Exception as e:
            raise Exception(f"Error generating QR code: {str(e)}")

    def save_qr(self, data, filename):
        """Save QR code to file"""
        try:
            img = self.generate_qr(data)
            img.save(filename)
            return True
        except Exception as e:
            raise Exception(f"Error saving QR code: {str(e)}")