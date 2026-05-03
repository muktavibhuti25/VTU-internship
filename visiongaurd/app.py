from flask import Flask, render_template, request
import os
from detect import process_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        file = request.files.get("video")

        if not file or file.filename == "":
            return "No file selected"

        input_path = os.path.join(UPLOAD_FOLDER, "input.mp4")
        file.save(input_path)

        # Remove old output
        output_file = os.path.join(OUTPUT_FOLDER, "output.avi")
        if os.path.exists(output_file):
            os.remove(output_file)

        # Process
        video_name = process_video(input_path, OUTPUT_FOLDER)

        if not video_name:
            return "Error processing video"

        return render_template("index.html", video=video_name)

    return render_template("index.html", video=None)


if __name__ == "__main__":
    app.run(debug=True)