from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route("/")
def home():
    response = requests.get("https://api.artic.edu/api/v1/artworks?fields=id,title,artist_display,date_display,main_reference_numb&page=1&limit=100")
    data = response.json()
    artworkList = data["data"]
    return render_template("index.html", artworkList=artworkList)
app.run(debug=True)

