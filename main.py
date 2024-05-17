from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

HOME_DIR = os.path.expanduser("~")
DESKTOP_DIR = os.path.join(HOME_DIR, 'Desktop')

DOWNLOAD_DIR = DESKTOP_DIR

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route("/download", methods=["POST"])
def download_video():
    video_url = request.json.get('video_url')

    if not video_url:
        logging.error("URL not found in request.")
        return jsonify({"message": 'URL not found'}), 400

    try:
        yt = YouTube(video_url)
        yd = yt.streams.get_highest_resolution()
        file_path = os.path.join(DOWNLOAD_DIR, yd.default_filename)
        logging.info(f"Starting download: {file_path}")
        yd.download(DOWNLOAD_DIR)
        logging.info(f"Downloaded successfully: {file_path}")
    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        return jsonify({"message": str(e)}), 400

    return jsonify({"title": yt.title, "views": yt.views, 'path': file_path}), 201

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=os.environ.get('PORT', 5000))
