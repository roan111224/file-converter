from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

    # Get selected format
    target_format = request.form["format"].upper()

    # Generate unique filename
    unique_id = str(uuid.uuid4())

    input_filename = f"{unique_id}_{file.filename}"
    input_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        input_filename
    )

    file.save(input_path)

    # Open image
    image = Image.open(input_path)

    # Pillow uses JPEG, not JPG
    if target_format == "JPG":
        save_format = "JPEG"
        extension = "jpg"
    else:
        save_format = target_format
        extension = target_format.lower()

    # JPEG cannot save transparency
    if save_format == "JPEG":
        image = image.convert("RGB")

    output_filename = (
        f"{unique_id}_converted.{extension}"
    )

    output_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        output_filename
    )

    image.save(output_path, save_format)

    return render_template(
        "result.html",
        filename=output_filename
    )


@app.route("/download/<filename>")
def download_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)