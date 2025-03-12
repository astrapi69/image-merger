import pytest
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Ensure the correct module path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../main/python")))

from mergeimg.merge_pdf_image import merge_pdf_image


@pytest.fixture
def test_files(tmp_path):
    """Creates temporary test files for PDF and signatures."""
    pdf_path = tmp_path / "test_document.pdf"
    signature_right_path = tmp_path / "signature_right.png"
    signature_left_path = tmp_path / "signature_left.png"
    output_pdf_path = tmp_path / "output_signed.pdf"

    # Create a valid PDF using reportlab
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    c.drawString(100, 750, "Test PDF Document")
    c.save()

    # Create dummy signature images
    from PIL import Image
    img = Image.new("RGB", (200, 80), color="white")
    img.save(signature_right_path)
    img.save(signature_left_path)

    return pdf_path, signature_right_path, signature_left_path, output_pdf_path


def test_merge_pdf_image(test_files):
    """Tests the merging of a PDF with signatures."""
    pdf_path, signature_right_path, signature_left_path, output_pdf_path = test_files

    result = merge_pdf_image(
        str(pdf_path), str(signature_right_path), str(signature_left_path), str(output_pdf_path)
    )

    assert result is not None
    assert os.path.exists(output_pdf_path)
    assert os.path.getsize(output_pdf_path) > 0
