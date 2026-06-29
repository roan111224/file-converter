import subprocess
import os


# LibreOffice executable path
LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"


def convert_document(input_path, output_folder):
    """
    Convert Office documents to PDF using LibreOffice.

    Supported input formats:
    - DOCX
    - DOC
    - ODT
    - RTF
    - TXT
    - PPTX
    - PPT
    - ODP
    - XLSX
    - XLS
    - ODS

    Output:
    - PDF
    """

    if not os.path.exists(LIBREOFFICE_PATH):
        raise FileNotFoundError(
            f"LibreOffice not found:\n{LIBREOFFICE_PATH}"
        )

    os.makedirs(output_folder, exist_ok=True)

    command = [
        LIBREOFFICE_PATH,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        output_folder,
        input_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(
            "LibreOffice conversion failed:\n"
            + result.stderr
        )

    filename = os.path.splitext(
        os.path.basename(input_path)
    )[0]

    output_pdf = os.path.join(
        output_folder,
        filename + ".pdf"
    )

    if not os.path.exists(output_pdf):
        raise Exception(
            "PDF was not created."
        )

    return output_pdf