import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image


class BarcodeGenerator:
    """Barcode generator for books"""

    def generate_barcode(self, data):
        """Generate barcode from data and return PIL Image"""
        try:
            if not data or not isinstance(data, str):
                raise ValueError("Data must be a non-empty string")

            # Use Code128 format which supports alphanumeric characters
            CODE = barcode.get_barcode_class('code128')
            code = CODE(data, writer=ImageWriter())

            # Save to BytesIO
            fp = BytesIO()
            code.write(fp)
            fp.seek(0)

            img = Image.open(fp)

            # Resize for display (barcodes are usually wider)
            img = img.resize((250, 120), Image.Resampling.LANCZOS)

            return img
        except Exception as e:
            raise Exception(f"Error generating barcode: {str(e)}")