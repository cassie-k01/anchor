from flask import send_from_directory
from app import create_app
import os

app = create_app()

frontend_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

@app.route("/frontend/<path:filename>")
def frontend(filename):
    return send_from_directory(frontend_folder, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)