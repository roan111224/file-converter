from PIL import Image
from pdf2image import convert_from_path
import os

# Your Poppler installation path
POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"


def convert_image(input_path, output_path, target_format):
    """
    Convert image and PDF files.

    Supported input:
    - JPG
    - JPEG
    - PNG
    - WEBP
    - PDF (first page)

    Supported output:
    - JPG
    - PNG
    - WEBP
    - PDF
    """

    # Detect input file type
    file_extension = os.path.splitext(input_path)[1].lower()

    # Open PDF
    if file_extension == ".pdf":

        pages = convert_from_path(
            input_path,
            poppler_path=POPPLER_PATH
        )

        image = pages[0]

    # Open image
    else:

        image = Image.open(input_path)

    # Output format
    target_format = target_format.upper()

    if target_format == "JPG":
        save_format = "JPEG"

    elif target_format == "PNG":
        save_format = "PNG"

    elif target_format == "WEBP":
        save_format = "WEBP"

    elif target_format == "PDF":
        save_format = "PDF"

    else:
        raise ValueError(f"Unsupported format: {target_format}")

    # JPEG and PDF require RGB mode
    if save_format in ["JPEG", "PDF"]:
        image = image.convert("RGB")

    # Save converted file
    image.save(output_path, save_format)