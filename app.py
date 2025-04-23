from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route("/")
def home():
    response = requests.get("https://api.artic.edu/api/v1/artworks?fields=id,title,image_id,artist_display,date_display,main_reference_numb&page=1&limit=10")
    data = response.json()
    artworkList = data["data"]
    return render_template("index.html", artworkList=artworkList)

@app.route("/artworks/<int:id>")
def artworkDetail():
    response = requests.get("/api/v1/artworks/{id}")
    data = response.json()

    title = data.get('title')
    artist = data.get('artist_display')
    origin = data.get('place_of_origin')
    
app.run(debug=True)

