import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image


class BarcodeGenerator:
    def generate_barcode(self, data):
        try:
            if not data or not isinstance(data, str):
                raise ValueError("Data must be a non-empty string")

            CODE = barcode.get_barcode_class('code128')
            code = CODE(data, writer=ImageWriter())

            fp = BytesIO()
            code.write(fp)
            fp.seek(0)

            img = Image.open(fp)
            img = img.resize((250, 120), Image.Resampling.LANCZOS)

            return img
        except Exception as e:
            raise Exception(f"Error generating barcode: {str(e)}")