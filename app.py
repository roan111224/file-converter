from flask import Flask, render_template, request, send_from_directory
from converters.image_converter import convert_image
from converters.document_converter import convert_document
from converters.audio_converter import convert_audio
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():

    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    target_format = request.form["format"].upper()

    unique_id = str(uuid.uuid4())

    filename = unique_id + "_" + file.filename

    input_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(input_path)

    extension = os.path.splitext(filename)[1].lower()

    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".pdf"
    ]

    document_extensions = [
        ".doc",
        ".docx",
        ".odt",
        ".rtf",
        ".txt",
        ".ppt",
        ".pptx",
        ".odp",
        ".xls",
        ".xlsx",
        ".ods"
    ]

    audio_extensions = [
        ".mp3",
        ".wav",
        ".flac",
        ".ogg",
        ".aac",
        ".m4a",
        ".wma",
        ".aiff"
    ]

    # -----------------------------
    # IMAGE CONVERTER
    # -----------------------------
    if extension in image_extensions:

        output_extension = target_format.lower()

        if target_format == "JPG":
            output_extension = "jpg"

        output_filename = (
            unique_id +
            "_converted." +
            output_extension
        )

        output_path = os.path.join(
            app.config["CONVERTED_FOLDER"],
            output_filename
        )

        convert_image(
            input_path,
            output_path,
            target_format
        )

    # -----------------------------
    # DOCUMENT CONVERTER
    # -----------------------------
    elif extension in document_extensions:

        if target_format != "PDF":
            return "Document files can currently be converted only to PDF."

        output_path = convert_document(
            input_path,
            app.config["CONVERTED_FOLDER"]
        )

        output_filename = os.path.basename(output_path)

    # -----------------------------
    # AUDIO CONVERTER
    # -----------------------------
    elif extension in audio_extensions:

        output_extension = target_format.lower()

        output_filename = (
            unique_id +
            "_converted." +
            output_extension
        )

        output_path = os.path.join(
            app.config["CONVERTED_FOLDER"],
            output_filename
        )

        convert_audio(
            input_path,
            output_path
        )

    else:

        return "Unsupported file type."

    return render_template(
        "result.html",
        filename=output_filename
    )


@app.route("/download/<filename>")
def download_file(filename):

    return send_from_directory(
        app.config["CONVERTED_FOLDER"],
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)