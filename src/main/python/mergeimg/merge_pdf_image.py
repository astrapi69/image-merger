from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import os


def merge_pdf_image(pdf_path, signature_asterios_path, signature_arevik_path, output_pdf_path):
    """
    Merges signatures as images into the last page of a PDF document.

    :param pdf_path: Path to the original PDF file
    :param signature_asterios_path: Path to Asterios' signature image
    :param signature_arevik_path: Path to Arevik's signature image
    :param output_pdf_path: Path to save the output PDF with signatures
    :return: Path to the generated PDF
    """
    try:
        # Load the original PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        # Create a temporary PDF for the signatures
        signature_pdf_path = "signatures_temp.pdf"
        c = canvas.Canvas(signature_pdf_path, pagesize=A4)

        # Load and resize signatures
        signature_asterios = Image.open(signature_asterios_path).resize((200, 80))
        signature_arevik = Image.open(signature_arevik_path).resize((200, 80))

        # Save resized signatures as temporary files
        signature_asterios_temp = "asterios_signature_temp.png"
        signature_arevik_temp = "arevik_signature_temp.png"

        signature_asterios.save(signature_asterios_temp)
        signature_arevik.save(signature_arevik_temp)

        # Draw signatures onto the new PDF page
        c.drawImage(signature_asterios_temp, 100, 150, mask='auto')  # Position for Asterios
        c.drawString(100, 130, "Asterios Raptis")

        c.drawImage(signature_arevik_temp, 300, 150, mask='auto')  # Position for Arevik
        c.drawString(300, 130, "Arevik Poghosyan")

        c.save()

        # Merge original PDF pages
        for page in reader.pages:
            writer.add_page(page)

        # Append the signature page
        signature_reader = PdfReader(signature_pdf_path)
        writer.add_page(signature_reader.pages[0])

        # Save the final PDF
        with open(output_pdf_path, 'wb') as f:
            writer.write(f)

        # Cleanup temporary files
        os.remove(signature_pdf_path)
        os.remove(signature_asterios_temp)
        os.remove(signature_arevik_temp)

        return output_pdf_path

    except Exception as e:
        print(f"Error merging PDF with images: {e}")
        return None
