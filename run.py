from flask import send_from_directory
from app import create_app
import os

app = create_app()

# Get the absolute path to the frontend folder
frontend_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

@app.route("/frontend/<path:filename>")
def frontend(filename):
    return send_from_directory(frontend_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)