import os
import subprocess

# Path to FFmpeg
FFMPEG_PATH = r"C:\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"


def convert_audio(input_path, output_path):
    """
    Convert one audio format to another using FFmpeg.
    The output format is determined by the extension of output_path.
    """

    if not os.path.exists(FFMPEG_PATH):
        raise FileNotFoundError(
            f"FFmpeg not found:\n{FFMPEG_PATH}"
        )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i",
        input_path,
        output_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(
            "FFmpeg conversion failed:\n"
            + result.stderr
        )

    if not os.path.exists(output_path):
        raise Exception(
            "Converted audio file was not created."
        )

    return output_path