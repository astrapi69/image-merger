import pytest
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from merge_pdf_image import merge_pdf_image


@pytest.fixture
def test_files(tmp_path):
    """Creates temporary test files for PDF and signatures."""
    pdf_path = tmp_path / "test_document.pdf"
    signature_asterios_path = tmp_path / "signature_asterios.png"
    signature_arevik_path = tmp_path / "signature_arevik.png"
    output_pdf_path = tmp_path / "output_signed.pdf"

    # Create a valid PDF using reportlab
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    c.drawString(100, 750, "Test PDF Document")
    c.save()

    # Create dummy signature images
    from PIL import Image
    img = Image.new("RGB", (200, 80), color="white")
    img.save(signature_asterios_path)
    img.save(signature_arevik_path)

    return pdf_path, signature_asterios_path, signature_arevik_path, output_pdf_path


def test_merge_pdf_image(test_files):
    """Tests the merging of a PDF with signatures."""
    pdf_path, signature_asterios_path, signature_arevik_path, output_pdf_path = test_files

    result = merge_pdf_image(
        str(pdf_path), str(signature_asterios_path), str(signature_arevik_path), str(output_pdf_path)
    )

    assert result is not None
    assert os.path.exists(output_pdf_path)
    assert os.path.getsize(output_pdf_path) > 0
