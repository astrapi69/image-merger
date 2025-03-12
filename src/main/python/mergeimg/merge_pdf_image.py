from pypdf import PdfReader, PdfWriter, PageObject  # Use pypdf instead of PyPDF2 (if not installed, use poetry add pypdf)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import os


def merge_pdf_image(pdf_path, signature_right_path, signature_left_path, output_pdf_path):
    """
    Merges signatures as images onto the last page of a PDF document.

    :param pdf_path: Path to the original PDF file
    :param signature_right_path: Path to right's signature image
    :param signature_left_path: Path to left's signature image
    :param output_pdf_path: Path to save the output PDF with signatures
    :return: Path to the generated PDF
    """
    try:
        # Load the original PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        # Get the last page
        last_page = reader.pages[-1]
        width, height = last_page.mediabox.width, last_page.mediabox.height

        # Create a temporary overlay PDF for the signatures
        signature_pdf_path = "signatures_overlay.pdf"
        c = canvas.Canvas(signature_pdf_path, pagesize=(width, height))

        # Load and resize signatures
        signature_right = Image.open(signature_right_path).resize((100, 80))
        signature_left = Image.open(signature_left_path).resize((100, 80))

        # Save resized signatures as temporary files
        signature_right_temp = "right_signature_temp.png"
        signature_left_temp = "left_signature_temp.png"

        signature_right.save(signature_right_temp)
        signature_left.save(signature_left_temp)

        # Overlay signatures on the last page at desired positions
        c.drawImage(signature_right_temp, width - 250, 80, mask='auto')  # Right signature position
        c.drawImage(signature_left_temp, 50, 80, mask='auto')  # Left signature position
        c.save()

        # Merge the overlay with the last page
        signature_reader = PdfReader(signature_pdf_path)
        last_page.merge_page(signature_reader.pages[0])  # Merge the signature overlay onto the last page

        # Add all pages to the writer, replacing the last page with the modified one
        for i, page in enumerate(reader.pages):
            writer.add_page(page if i < len(reader.pages) - 1 else last_page)

        # Save the final PDF
        with open(output_pdf_path, 'wb') as f:
            writer.write(f)

        # Cleanup temporary files
        os.remove(signature_pdf_path)
        os.remove(signature_right_temp)
        os.remove(signature_left_temp)

        return output_pdf_path

    except Exception as e:
        print(f"Error merging PDF with images: {e}")
        return None
