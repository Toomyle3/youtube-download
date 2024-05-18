from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

def normalize_path(path):
    normalized_path = path.replace("/", "\\")
    return normalized_path

@app.route("/download", methods=["POST"])
def download_video():
    video_url = request.json.get('video_url')
    download_directory = request.json.get('download_directory')

    if not video_url:
        logging.error("URL not found in request.")
        return jsonify({"message": 'URL not found'}), 400

    try:
        yt = YouTube(video_url)
        if yt is None or yt.title == "Video Not Available":
            raise ValueError("The video is not available.")
        yd = yt.streams.get_highest_resolution()
        path = os.path.join(download_directory, yd.default_filename)
        file_path = normalize_path(path)
        yd.download(download_directory)
        logging.info(f"Downloaded successfully: {file_path}")
        return jsonify({"title": yt.title, "views": yt.views, 'path': file_path}), 201
    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        return jsonify({"message": "An error occurred while downloading the video."}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
