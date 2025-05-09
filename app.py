from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route("/")
def home():
    response = requests.get("https://api.artic.edu/api/v1/artworks?fields=id,title,image_id,artist_display,date_display,main_reference_numb&page=1&limit=50")
    data = response.json()
    artworkList = data["data"]
    return render_template("index.html", artworkList=artworkList)

@app.route("/artworks/<int:id>")
def artworkDetail(id):
    response = requests.get(f"https://api.artic.edu/api/v1/artworks/{id}")
    data = response.json()
    artworkData = data.get("data", {})

    title = artworkData.get('title')
    artist = artworkData.get('artist_display')
    origin = artworkData.get('place_of_origin')
    imageId = artworkData.get('image_id')
    date = artworkData.get('date_start')
    description = artworkData.get('short_description')
    if description == None:
        description = ''
    medium = artworkData.get('medium_display')
    department = artworkData.get('department_title') 
    imageUrl = f"https://www.artic.edu/iiif/2/{imageId}/full/843,/0/default.jpg" 
    return render_template("artwork.html", artwork = {
        'title': title, 
        'artist': artist, 
        'origin': origin,
        'image' : imageUrl,
        'date': date,
        'description': description,
        'medium': medium,
        'department': department,
    })
if __name__ == '__main__':
    app.run(debug=True)
