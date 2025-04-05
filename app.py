from flask import Flask, render_template, requests
app = Flask(__name__)

@app.route("/")
def home():
    response = requests.get("https://openlibrary.org/developers/api?limit=200")
    data = response.json()
