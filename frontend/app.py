from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "http://localhost:8000/chat"

@app.route("/", methods=["GET"])
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    form = request.form.to_dict()
    files = {"file": request.files["file"]} if "file" in request.files else None
    response = requests.post(API_URL, data=form, files=files)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
