from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route("/")
def home():
    response = requests.get("https://api.artic.edu/api/v1/artworks?fields=id,title,artist_display,date_display,main_reference_numb&page=1&limit=10")
    data = response.json()
    artworkList = data["data"]
    for artwork in artworkList:
        Url = requests.get(f"https://api.artic.edu/api/v1/artworks/{artwork["id"]}?fields=id,title,image_id")
        imageData = Url.json()
        id = imageData["data"]["image_id"]
        iiifUrl = imageData["config"]["iiif_url"]
        imageUrl = iiifUrl.append(id)
    return render_template("index.html", artworkList=artworkList, imageUrl = imageUrl)
app.run(debug=True)

