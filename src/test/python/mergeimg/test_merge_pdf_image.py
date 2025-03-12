import pytest
import os
import shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Ensure the correct module path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../main/python")))

from mergeimg.merge_pdf_image import merge_pdf_image

# Flag to keep or delete test files after test execution
KEEP_FILES = True  # Set to False to delete files after the test


@pytest.fixture(scope="session")
def test_files():
    """Creates test files for PDF and signatures inside src/test/resources/."""
    resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources"))
    os.makedirs(resources_dir, exist_ok=True)

    pdf_path = os.path.join(resources_dir, "test_document.pdf")
    signature_right_path = os.path.join(resources_dir, "signature_right.png")
    signature_left_path = os.path.join(resources_dir, "signature_left.png")
    output_pdf_path = os.path.join(resources_dir, "output_signed.pdf")

    print("\n[Setup] Creating test files in src/test/resources/...")

    # Ensure test files are created if they do not exist or are empty
    def create_file_if_needed(file_path, create_func):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            create_func(file_path)
            print(f"[Created] {file_path}")
        else:
            print(f"[Skipped] {file_path} already exists and is not empty.")

    # Create a valid PDF using reportlab
    def create_pdf(file_path):
        c = canvas.Canvas(file_path, pagesize=A4)
        c.drawString(100, 750, "Test PDF Document")
        c.save()

    create_file_if_needed(pdf_path, create_pdf)

    # Create dummy signature images
    def create_image(file_path):
        from PIL import Image
        img = Image.new("RGB", (200, 80), color="white")
        img.save(file_path)

    create_file_if_needed(signature_right_path, create_image)
    create_file_if_needed(signature_left_path, create_image)

    return pdf_path, signature_right_path, signature_left_path, output_pdf_path


def test_merge_pdf_image(test_files):
    """Tests the merging of a PDF with signatures and ensures output PDF is retained."""
    pdf_path, signature_right_path, signature_left_path, output_pdf_path = test_files

    print("\n[Start] Running merge_pdf_image function...")

    result = merge_pdf_image(
        str(pdf_path), str(signature_right_path), str(signature_left_path), str(output_pdf_path)
    )

    print("[Check] Verifying output...")

    # Check if result is returned
    assert result is not None, "Error: merge_pdf_image function returned None!"

    # Check if the output file exists
    assert os.path.exists(output_pdf_path), f"Error: Output PDF does not exist! Expected at {output_pdf_path}"

    # Check if the output PDF is not empty
    output_size = os.path.getsize(output_pdf_path)
    assert output_size > 0, "Error: Output PDF is empty!"

    print(f"[Success] Output PDF generated successfully at: {output_pdf_path} (Size: {output_size} bytes)")

    print(f"[Saved] Output PDF is stored at: {output_pdf_path}")

    # Cleanup if flag is set to False
    if not KEEP_FILES:
        for file in [pdf_path, signature_right_path, signature_left_path, output_pdf_path]:
            if os.path.exists(file):
                os.remove(file)
                print(f"[Cleanup] Deleted: {file}")


def test_merge_pdf_image_no_overwrite(test_files):
    """Ensures that existing non-empty files are not overwritten."""
    pdf_path, signature_right_path, signature_left_path, output_pdf_path = test_files

    # Check if the output file already exists and is non-empty
    if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
        print(f"[Skipped] {output_pdf_path} already exists and is not empty. Skipping merge.")
        return

    print("\n[Start] Running merge_pdf_image function for non-overwrite test...")

    result = merge_pdf_image(
        str(pdf_path), str(signature_right_path), str(signature_left_path), str(output_pdf_path)
    )

    print("[Check] Verifying output...")

    assert result is not None, "Error: merge_pdf_image function returned None!"
    assert os.path.exists(output_pdf_path), f"Error: Output PDF does not exist! Expected at {output_pdf_path}"
    assert os.path.getsize(output_pdf_path) > 0, "Error: Output PDF is empty!"

    print(f"[Success] Output PDF generated successfully at: {output_pdf_path} (Size: {os.path.getsize(output_pdf_path)} bytes)")
