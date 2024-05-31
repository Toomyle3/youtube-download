from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
import tkinter as tk
from tkinter import filedialog
import os
import threading
import logging

root = tk.Tk()
root.withdraw()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

def perform_download(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        highest_res_stream = streams.get_highest_resolution()
        highest_res_stream.download(output_path=save_path)
        logging.info("Video downloaded successfully!")
        return {"title": yt.title, "views": yt.views, "path": save_path}
    except Exception as e:
        logging.error(f"Download error: {e}")
        return None

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        logging.info(f"Selected folder: {folder}")
    return folder

@app.route("/download", methods=["POST"])
def handle_download_request():
    video_url = request.json.get('video_url')
    
    if not video_url:
        logging.error("URL not found in request.")
        return jsonify({"message": "URL not found"}), 400
    
    save_dir = open_file_dialog()
    if not save_dir:
        logging.error("No directory selected.")
        return jsonify({"message": "No directory selected"}), 400

    try:
        result = perform_download(video_url, save_dir)
        if result:
            return jsonify(result), 201
        else:
            return jsonify({"message": "An error occurred while downloading the video."}), 400
    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        return jsonify({"message": "An error occurred while downloading the video."}), 400

# Run the Flask app in a separate thread
def run_flask_app():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    root.mainloop()